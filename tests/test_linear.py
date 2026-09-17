"""Linear backend invariants (2026-09-17 Todoist/Google Tasks -> Linear migration).

Fake transport only (linear._graphql is monkeypatched). Pins: fail-closed without a key,
no fallback to Todoist/Google Tasks, idempotent create via capture-id lookup, alias and
unknown-project routing, lossless long titles and timed dues, the telegram +t lane, the
linear-complete button verb, and command routing (done / refresh / pull) under the
linear backend.
"""
from __future__ import annotations

import argparse
import json
from unittest.mock import MagicMock

import pytest

from todo_cli import commands, linear, telegram, todoist
from todo_cli.models import LinearSync, TodoEntry, TodoistSync
from todo_cli.storage import load_all, write_all

TEAM = {"teams": {"nodes": [{"id": "team-1", "key": "NAT", "name": "Nathanmauro"}]}}
STATES = {"team": {"states": {"nodes": [
    {"id": "st-backlog", "name": "Backlog", "type": "backlog"},
    {"id": "st-todo", "name": "Todo", "type": "unstarted"},
    {"id": "st-prog", "name": "In Progress", "type": "started"},
    {"id": "st-done", "name": "Done", "type": "completed"},
]}}}
PROJECTS = {"team": {"projects": {"nodes": [
    {"id": "p-personal", "name": "Personal"},
    {"id": "p-blackbox", "name": "Black Box"},
    {"id": "p-todo", "name": "Todo CLI & Telegram"},
    {"id": "p-career", "name": "Career Launchpad"},
    {"id": "p-cockpit", "name": "Cockpit"},
]}}}
LABELS = {"issueLabels": {"nodes": [
    {"id": "l-capture", "name": "capture"}, {"id": "l-idea", "name": "idea"},
]}}


class FakeLinear:
    """Records every GraphQL call; serves lookups and creates like the real API."""

    def __init__(self, *, existing: dict | None = None, lose_response_once: bool = False):
        self.calls: list[tuple[str, dict]] = []
        self.created: list[dict] = []
        self.existing = existing or {}  # capture-id -> issue
        self.lose_response_once = lose_response_once
        self.completed: list[str] = []

    def __call__(self, query: str, variables: dict | None = None) -> dict:
        variables = variables or {}
        self.calls.append((query, variables))
        if "teams(filter" in query:
            return TEAM
        if "states{" in query:
            return STATES
        if "projects(first" in query:
            return PROJECTS
        if "issueLabels" in query:
            return LABELS
        if "issue(id:" in query:
            iid = variables.get("id")
            hit = next((i for i in self.existing.values() if i.get("id") == iid), None)
            return {"issue": dict(hit) if hit else None}
        if "issues(first:5" in query:
            needle = variables["needle"].replace("capture-id: ", "")
            hit = self.existing.get(needle)
            return {"issues": {"nodes": [hit] if hit else []}}
        if "issueCreate" in query:
            inp = variables["input"]
            n = len(self.created) + 1
            issue = {"id": inp.get("id") or f"uuid-{n}", "identifier": f"NAT-{900 + n}", "url": f"https://linear.app/x/NAT-{900 + n}"}
            self.created.append(inp)
            cid = inp["description"].rsplit("capture-id: ", 1)[-1].rstrip("_ \n")
            self.existing[cid] = issue
            if self.lose_response_once:
                self.lose_response_once = False
                raise linear.LinearError("Linear unreachable: response lost after create")
            return {"issueCreate": {"success": True, "issue": issue}}
        if "issueUpdate" in query:
            self.completed.append(variables["id"])
            return {"issueUpdate": {"success": True}}
        raise AssertionError(f"unexpected query: {query[:60]}")


@pytest.fixture(autouse=True)
def _linear_env(monkeypatch):
    monkeypatch.setenv("TODO_TASK_BACKEND", "linear")
    monkeypatch.setenv("TODO_LINEAR_API_KEY", "lin_test_key")
    linear.reset_cache()
    yield
    linear.reset_cache()


@pytest.fixture
def fake(monkeypatch):
    f = FakeLinear()
    monkeypatch.setattr(linear, "_graphql", f)
    return f


# --- transport / auth --------------------------------------------------------

def test_graphql_sends_bare_personal_key_header(monkeypatch):
    seen = {}

    class Resp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps({"data": {"ok": 1}}).encode()

    def fake_urlopen(req, timeout=0):
        seen["auth"] = req.get_header("Authorization")
        seen["body"] = json.loads(req.data)
        return Resp()

    monkeypatch.setattr(linear.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(linear.json, "load", lambda fh: json.loads(fh.read()))
    assert linear._graphql("query{ ok }") == {"ok": 1}
    assert seen["auth"] == "lin_test_key"          # no "Bearer " prefix for personal keys
    assert seen["body"]["query"] == "query{ ok }"


def test_no_key_fails_closed_and_keeps_row(monkeypatch, fake):
    monkeypatch.delenv("TODO_LINEAR_API_KEY")
    monkeypatch.setattr(linear, "token", lambda: None)
    entries = [TodoEntry(text="keep me", source="cli")]
    assert linear.sync(entries, quiet=True) == 1
    assert entries[0].sync.linear is None
    assert fake.created == []                      # nothing sent anywhere
    assert entries[0].sync.todoist is None and entries[0].sync.gtasks is None


# --- create semantics --------------------------------------------------------

def test_sync_creates_with_capture_id_and_is_idempotent(fake):
    entries = [TodoEntry(text="push me", source="cli", due="2026-09-20")]
    assert linear.sync(entries, quiet=True) == 0
    assert len(fake.created) == 1
    inp = fake.created[0]
    assert inp["teamId"] == "team-1" and inp["projectId"] == "p-personal"
    assert inp["stateId"] == "st-todo" and inp["labelIds"] == ["l-capture"]
    assert inp["dueDate"] == "2026-09-20" and inp["priority"] == 0
    assert f"capture-id: {entries[0].id}" in inp["description"]
    assert entries[0].sync.linear.identifier == "NAT-901"
    # second run: stamped -> no-op
    assert linear.sync(entries, quiet=True) == 0
    assert len(fake.created) == 1


def test_lost_response_then_retry_adopts_instead_of_duplicating(monkeypatch):
    fake = FakeLinear(lose_response_once=True)
    monkeypatch.setattr(linear, "_graphql", fake)
    entries = [TodoEntry(text="flaky network")]
    # Linear created the issue but the response was lost: the deterministic id lets the
    # same run re-check by id and adopt, so the row is stamped with ONE create.
    assert linear.sync(entries, quiet=True) == 0
    assert len(fake.created) == 1
    assert entries[0].sync.linear.identifier == "NAT-901"
    assert fake.created[0]["id"] == linear.issue_uuid(entries[0].id)
    # a later retry is a no-op (stamped), and even an unstamped twin adopts instead of creating
    twin = TodoEntry(id=entries[0].id, text="flaky network")
    assert linear.sync([twin], quiet=True) == 0
    assert len(fake.created) == 1 and twin.sync.linear.identifier == "NAT-901"


def test_skips_rows_other_backends_already_have(fake):
    stamped = TodoEntry(text="already in todoist")
    stamped.sync.todoist = TodoistSync(task_id="T1", ts="x")
    mirrored = TodoEntry(text="mirrored", origin="todoist")
    done = TodoEntry(text="done", status="done")
    assert linear.sync([stamped, mirrored, done], quiet=True) == 0
    assert fake.created == []


def test_project_alias_and_exact_name(fake):
    rows = [
        TodoEntry(text="a", project="sba-agentic"),
        TodoEntry(text="b", project="todo"),
        TodoEntry(text="c", project="employment"),
        TodoEntry(text="d", project="black box"),
        TodoEntry(text="e"),
    ]
    assert linear.sync(rows, quiet=True) == 0
    assert [i["projectId"] for i in fake.created] == ["p-blackbox", "p-todo", "p-career", "p-blackbox", "p-personal"]


def test_unknown_project_queues_with_routing_error(fake):
    row = TodoEntry(text="mystery", project="no-such-project")
    assert linear.sync([row], quiet=True) == 1
    assert fake.created == [] and row.sync.linear is None
    with pytest.raises(linear.RoutingError):
        linear.resolve_project("no-such-project")


def test_missing_default_project_fails_closed(monkeypatch, fake):
    monkeypatch.setattr(linear, "LINEAR_DEFAULT_PROJECT", "Nope")
    row = TodoEntry(text="homeless")
    assert linear.sync([row], quiet=True) == 1
    assert fake.created == [] and row.sync.linear is None


def test_long_title_and_timed_due_are_preserved(fake):
    text = "x" * 300
    row = TodoEntry(text=text, due="2026-09-18T09:00:00", priority="p2", dest="idea")
    assert linear.sync([row], quiet=True) == 0
    inp = fake.created[0]
    assert len(inp["title"]) == 255 and inp["title"].endswith("…")
    assert text in inp["description"]              # full capture kept
    assert inp["dueDate"] == "2026-09-18"
    assert "`2026-09-18T09:00:00`" in inp["description"] and "date-only" in inp["description"]
    assert inp["priority"] == 2 and inp["stateId"] == "st-backlog"
    assert set(inp["labelIds"]) == {"l-capture", "l-idea"}


def test_completions_pushed_once(fake):
    row = TodoEntry(text="finish", status="done")
    row.sync.linear = LinearSync(issue_id="uuid-7", identifier="NAT-7", ts="x")
    assert linear.push_completions([row]) == (1, 0)
    assert fake.completed == ["uuid-7"] and row.sync.linear.closed_ts
    assert linear.push_completions([row]) == (0, 0)


# --- telegram +t lane --------------------------------------------------------

def test_push_task_linear_success_stamps(fake):
    assert telegram._push_task("buy milk", source="telegram") is True
    [row] = load_all()
    assert row.sync.linear.identifier == "NAT-901" and row.sync.todoist is None
    assert f"capture-id: {row.id}" in fake.created[0]["description"]


def test_push_task_linear_fail_closed_no_key(monkeypatch, fake):
    monkeypatch.setattr(linear, "token", lambda: None)
    assert telegram._push_task("do not lose me", source="telegram") is False
    [row] = load_all()
    assert row.text == "do not lose me" and row.sync.linear is None
    assert fake.created == []
    # once a key exists the queued row drains without duplication
    monkeypatch.setattr(linear, "token", lambda: "lin_key")
    entries = load_all()
    assert linear.sync(entries, quiet=True) == 0
    assert len(fake.created) == 1 and entries[0].sync.linear


def test_push_task_never_falls_back_to_todoist(monkeypatch, fake):
    monkeypatch.setattr(linear, "create_issue", MagicMock(side_effect=linear.LinearError("boom")))
    todoist_create = MagicMock()
    monkeypatch.setattr(todoist, "create_task", todoist_create)
    assert telegram._push_task("x", source="telegram") is False
    assert todoist_create.call_count == 0


def test_backend_name_and_verb():
    assert telegram._task_backend_name() == "Linear"
    assert "linear-complete" in telegram.ACTION_VERBS


def test_linear_complete_flips_local_row(fake):
    row = TodoEntry(text="tap me")
    row.sync.linear = LinearSync(issue_id="uuid-3", identifier="NAT-3", ts="x")
    write_all([row])
    assert telegram._execute_action({"verb": "linear-complete", "payload": "NAT-3"}) == "done ✓"
    assert fake.completed == ["NAT-3"]
    [back] = load_all()
    assert back.status == "done" and back.sync.linear.closed_ts


def test_linear_complete_bad_payload(fake):
    assert telegram._linear_complete("bad payload!") == "bad linear payload"
    assert fake.completed == []


# --- command routing ---------------------------------------------------------

def test_cmd_done_routes_completion_to_linear(monkeypatch, fake):
    row = TodoEntry(text="close me")
    row.sync.linear = LinearSync(issue_id="uuid-9", identifier="NAT-9", ts="x")
    write_all([row])
    todoist_push = MagicMock(return_value=(0, 0))
    monkeypatch.setattr(todoist, "push_completions", todoist_push)
    assert commands.cmd_done(argparse.Namespace(id_prefix=row.short_id)) == 0
    assert fake.completed == ["uuid-9"] and todoist_push.call_count == 0
    [back] = load_all()
    assert back.status == "done" and back.sync.linear.closed_ts


def test_refresh_skips_todoist_and_drains_linear(monkeypatch, fake):
    write_all([TodoEntry(text="queued while offline", source="telegram")])
    boom = MagicMock(side_effect=AssertionError("Todoist must not be touched"))
    monkeypatch.setattr(todoist, "mirror", boom)
    monkeypatch.setattr(todoist, "reconcile", boom)
    assert commands.cmd_refresh(argparse.Namespace(dry_run=False)) == 0
    [row] = load_all()
    assert row.sync.linear.identifier == "NAT-901"
    assert commands.cmd_refresh(argparse.Namespace(dry_run=True)) == 0


def test_pull_is_noop_under_linear(monkeypatch, capsys):
    boom = MagicMock(side_effect=AssertionError("Todoist must not be touched"))
    monkeypatch.setattr(todoist, "mirror", boom)
    assert commands.cmd_pull(argparse.Namespace(dry_run=False)) == 0
    assert "frozen source" in capsys.readouterr().out


def test_add_carries_priority_dest_project(monkeypatch, fake):
    args = argparse.Namespace(text=["ship", "it"], source="codex", due=None, project="cockpit",
                              priority="p1", dest="current", notes="Queued by codex\nQueue file: q.json", no_sync=False)
    assert commands.cmd_add(args) == 0
    [row] = load_all()
    assert row.priority == "p1" and row.dest == "current" and row.project == "cockpit"
    inp = fake.created[0]
    assert inp["projectId"] == "p-cockpit" and inp["stateId"] == "st-prog" and inp["priority"] == 1
    assert "Queue file: q.json" in inp["description"] and inp["title"] == "ship it"


# --- hardening: stable ids, races, retired targets, unknown backend, legacy verbs, adoption, views ---

def test_create_input_carries_deterministic_issue_id(fake):
    row = TodoEntry(text="stable")
    assert linear.sync([row], quiet=True) == 0
    assert fake.created[0]["id"] == linear.issue_uuid(row.id)
    assert fake.created[0]["id"] == linear.issue_uuid(row.id)  # deterministic
    import uuid as _uuid
    u = _uuid.UUID(fake.created[0]["id"])
    assert u.version == 4 and u.variant == _uuid.RFC_4122   # Linear validates client ids as v4


def test_graphql_error_includes_extensions_detail(monkeypatch):
    class Resp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps({"errors": [{"message": "Argument Validation Error", "extensions": {"userPresentableMessage": "id must be a UUID v4"}}]}).encode()
    monkeypatch.setattr(linear.urllib.request, "urlopen", lambda req, timeout=0: Resp())
    monkeypatch.setattr(linear.json, "load", lambda fh: json.loads(fh.read()))
    with pytest.raises(linear.LinearError) as exc:
        linear._graphql("mutation{ x }")
    assert "id must be a UUID v4" in str(exc.value)


def test_overlapping_create_adopts_by_id(monkeypatch):
    """Two writers race the same row: Linear rejects the second create (same id) and it adopts."""
    fake = FakeLinear()
    monkeypatch.setattr(linear, "_graphql", fake)
    row_a = TodoEntry(text="raced")
    row_b = row_a.model_copy(deep=True)
    assert linear.sync([row_a], quiet=True) == 0
    issue_id = fake.created[0]["id"]

    real = fake.__call__

    def by_id_aware(query, variables=None):
        if "issue(id:" in query and variables and variables.get("id") == issue_id:
            return {"issue": {"id": issue_id, "identifier": "NAT-901", "url": "u"}}
        if "issueCreate" in query:
            raise linear.LinearError("Linear GraphQL error: entity already exists")
        return real(query, variables)

    monkeypatch.setattr(linear, "_graphql", by_id_aware)
    assert linear.sync([row_b], quiet=True) == 0
    assert row_b.sync.linear.identifier == "NAT-901"
    assert len(fake.created) == 1


def test_sync_refuses_retired_targets_under_linear(monkeypatch, fake, capsys):
    monkeypatch.setattr(todoist, "sync", MagicMock(side_effect=AssertionError("Todoist must not be called")))
    write_all([TodoEntry(text="x")])
    assert commands.cmd_sync(argparse.Namespace(target="todoist")) == 2
    assert "retired" in capsys.readouterr().err
    assert commands.cmd_sync(argparse.Namespace(target="linear")) == 0
    assert len(fake.created) == 1


def test_unknown_backend_fails_closed(monkeypatch, fake, capsys):
    monkeypatch.setenv("TODO_TASK_BACKEND", "linera")
    monkeypatch.setattr(todoist, "sync", MagicMock(side_effect=AssertionError("Todoist must not be called")))
    write_all([TodoEntry(text="x")])
    assert commands.cmd_sync(argparse.Namespace(target="all")) == 2
    assert "not a known backend" in capsys.readouterr().err
    assert fake.created == []
    tc = MagicMock()
    monkeypatch.setattr(todoist, "create_task", tc)
    assert telegram._push_task("typo backend", source="telegram") is False
    assert tc.call_count == 0 and fake.created == []


def test_legacy_complete_verbs_refused_under_linear(monkeypatch, fake):
    from todo_cli import gtasks
    td = MagicMock(); gt = MagicMock()
    monkeypatch.setattr(todoist, "push_completions", td)
    monkeypatch.setattr(gtasks, "complete_task", gt)
    assert "retired" in telegram._execute_action({"verb": "todoist-complete", "payload": "abcdef12"})
    assert "retired" in telegram._execute_action({"verb": "gtasks-complete", "payload": "L1:G9"})
    assert td.call_count == 0 and gt.call_count == 0 and fake.completed == []


def test_linear_adopt_stamps_migrated_rows(tmp_path, fake, capsys):
    mirrored = TodoEntry(text="migrated", origin="todoist")
    mirrored.sync.todoist = TodoistSync(task_id="6TESTFINANCE0001", ts="x")
    orphan = TodoEntry(text="unmapped", origin="todoist")
    orphan.sync.todoist = TodoistSync(task_id="nomap", ts="x")
    local = TodoEntry(text="local capture")
    write_all([mirrored, orphan, local])
    m = tmp_path / "map.json"
    m.write_text(json.dumps({"issues": {"todoist:6TESTFINANCE0001": {"identifier": "NAT-99", "uuid": "9765-uuid", "url": "https://linear.app/x/NAT-99"}}}))
    assert commands.cmd_linear_adopt(argparse.Namespace(map=str(m), dry_run=True)) == 0
    assert load_all()[0].sync.linear is None  # dry-run wrote nothing
    assert commands.cmd_linear_adopt(argparse.Namespace(map=str(m), dry_run=False)) == 0
    rows = load_all()
    assert rows[0].sync.linear.issue_id == "9765-uuid" and rows[0].sync.linear.identifier == "NAT-99"
    assert rows[1].sync.linear is None and rows[2].sync.linear is None
    assert "adopted 1" in capsys.readouterr().out
    # now `todo done` on the migrated row closes the Linear issue
    assert commands.cmd_done(argparse.Namespace(id_prefix=rows[0].short_id)) == 0
    assert fake.completed == ["9765-uuid"]


def test_done_without_linear_link_says_so(fake, capsys):
    row = TodoEntry(text="never pushed", origin="todoist")
    row.sync.todoist = TodoistSync(task_id="T1", ts="x")
    write_all([row])
    assert commands.cmd_done(argparse.Namespace(id_prefix=row.short_id)) == 0
    out = capsys.readouterr().out
    assert "not closed in Linear" in out and fake.completed == []


def test_ls_pending_and_backlog_retired(fake, capsys, monkeypatch):
    queued = TodoEntry(text="queued")
    pushed = TodoEntry(text="pushed"); pushed.sync.linear = LinearSync(issue_id="u", identifier="NAT-1", ts="x")
    mirrored = TodoEntry(text="mirror", origin="todoist"); mirrored.sync.todoist = TodoistSync(task_id="T", ts="x")
    write_all([queued, pushed, mirrored])
    assert commands.cmd_ls(argparse.Namespace(filter="pending")) == 0
    cap = capsys.readouterr()
    assert "queued" in cap.out and "pushed" not in cap.out and "mirror" not in cap.out
    assert "1 row(s) pending delivery" in cap.err
    assert commands.cmd_backlog(argparse.Namespace(name="cockpit", json_output=True, if_project=False)) == 0
    payload = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert payload["retired"] is True and payload["project"] == "cockpit"
    # the real argparse surface, end to end
    import sys as _sys
    from todo_cli.cli import main as cli_main
    monkeypatch.setattr(_sys, "argv", ["todo", "backlog", "cockpit", "--json"])
    assert cli_main() == 0
    assert json.loads(capsys.readouterr().out.strip().splitlines()[-1])["retired"] is True


def test_add_with_stable_id_is_idempotent(fake):
    args = dict(text=["from", "queue"], source="codex", due=None, project=None, priority=None, dest=None, notes=None, no_sync=False)
    assert commands.cmd_add(argparse.Namespace(row_id="f66d1de6-1080-4c34-86c6-6b2f9e1acf4b", **args)) == 0
    assert commands.cmd_add(argparse.Namespace(row_id="f66d1de6-1080-4c34-86c6-6b2f9e1acf4b", **args)) == 0
    rows = load_all()
    assert len(rows) == 1 and rows[0].id == "f66d1de6-1080-4c34-86c6-6b2f9e1acf4b"
    assert len(fake.created) == 1 and fake.created[0]["id"] == linear.issue_uuid(rows[0].id)


def test_linear_adopt_never_replays_stale_local_completion(tmp_path, fake):
    """A row done locally (June) whose Linear issue is deliberately Todo must not be closed by adoption+refresh."""
    stale = TodoEntry(text="Rework /jaws", origin="todoist", status="done", done_ts="2026-06-10T00:00:00", done_source="local")
    stale.sync.todoist = TodoistSync(task_id="6TESTJAWS0000001", ts="x")
    write_all([stale])
    m = tmp_path / "map.json"
    m.write_text(json.dumps({"issues": {"todoist:6TESTJAWS0000001": {"identifier": "NAT-85", "uuid": "nat85-uuid", "url": "u"}}}))
    assert commands.cmd_linear_adopt(argparse.Namespace(map=str(m), dry_run=False)) == 0
    [row] = load_all()
    assert row.sync.linear.identifier == "NAT-85" and row.sync.linear.closed_ts  # already reconciled
    assert linear.completion_candidates([row]) == []
    assert commands.cmd_refresh(argparse.Namespace(dry_run=False)) == 0
    assert fake.completed == []                    # NAT-85 untouched
