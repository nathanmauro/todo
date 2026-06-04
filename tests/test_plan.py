"""`todo plan` — the idea→plan gate.

Pins the surgical frontmatter mutation (status + project only, body preserved),
idea resolution (exact / fuzzy / ambiguous / missing), idempotency, dry-run, and
the downstream contract: a planned idea shows under Planned and matches its
project exactly via the authoritative `project:` key.
"""
from __future__ import annotations

import json

import todo_cli.backlog as backlog
import todo_cli.plan as plan


def _ideas(tmp_path):
    d = tmp_path / "05 Notes" / "ideas"
    d.mkdir(parents=True)
    return d


def _idea(folder, name, frontmatter, body):
    fm = "".join(f"{k}: {v}\n" for k, v in frontmatter.items())
    p = folder / name
    p.write_text(f"---\n{fm}---\n\n{body}\n")
    return p


def _patch_vault(monkeypatch, tmp_path, projects=("constellate", "todo")):
    monkeypatch.setattr(plan, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(plan, "taxonomy_labels", lambda: {"projects": list(projects)})


# --- the mutation ------------------------------------------------------------

def test_shape_stamps_frontmatter_and_strip(tmp_path, monkeypatch):
    d = _ideas(tmp_path)
    p = _idea(d, "idea-foo.md",
              {"id": "idea-foo", "type": "idea", "status": "open", "tags": "[idea, x]"},
              "# Foo\n\n**Status:** Raw · **Heat:** Hot · **Domain:** Tooling\n\nspark")
    _patch_vault(monkeypatch, tmp_path)
    assert plan.shape("foo", "constellate") == 0
    out = p.read_text()
    assert "status: shaped" in out
    assert "project: constellate" in out
    assert "**Status:** Shaped" in out
    # untouched content preserved
    assert "id: idea-foo" in out
    assert "tags: [idea, x]" in out
    assert "spark" in out
    assert "**Heat:** Hot" in out


def test_shape_adds_project_key_when_absent(tmp_path, monkeypatch):
    d = _ideas(tmp_path)
    p = _idea(d, "idea-bar.md",
              {"id": "idea-bar", "type": "idea", "status": "open", "tags": "[idea]"},
              "# Bar\n\nspark only, no status strip")
    _patch_vault(monkeypatch, tmp_path)
    assert plan.shape("bar", "todo") == 0
    out = p.read_text()
    assert "project: todo" in out
    assert "status: shaped" in out


def test_dry_run_does_not_write(tmp_path, monkeypatch, capsys):
    d = _ideas(tmp_path)
    p = _idea(d, "idea-foo.md",
              {"id": "idea-foo", "type": "idea", "status": "open", "tags": "[idea]"},
              "# Foo\n\nspark")
    before = p.read_text()
    _patch_vault(monkeypatch, tmp_path)
    assert plan.shape("foo", "constellate", dry_run=True) == 0
    assert p.read_text() == before                      # unchanged
    assert "dry-run" in capsys.readouterr().out


def test_idempotent(tmp_path, monkeypatch, capsys):
    d = _ideas(tmp_path)
    _idea(d, "idea-foo.md",
          {"id": "idea-foo", "type": "idea", "status": "open", "tags": "[idea]"},
          "# Foo\n\nspark")
    _patch_vault(monkeypatch, tmp_path)
    plan.shape("foo", "constellate")
    capsys.readouterr()
    assert plan.shape("foo", "constellate") == 0        # second time: no-op
    assert "already planned" in capsys.readouterr().out


def test_status_strip_only_leading_line(tmp_path, monkeypatch):
    """Regression: only the leading strip flips to Shaped — never a mid-prose
    mention or a `**Status:**` line inside a code fence."""
    d = _ideas(tmp_path)
    body = (
        "# Foo\n\n"
        "**Status:** Raw · **Heat:** Hot · **Domain:** Tooling\n\n"
        "In prose we mention `**Status:** Cooking` as an example.\n\n"
        "```\n**Status:** Parked\n```"
    )
    p = _idea(d, "idea-foo.md",
              {"id": "idea-foo", "type": "idea", "status": "open", "tags": "[idea]"},
              body)
    _patch_vault(monkeypatch, tmp_path)
    assert plan.shape("foo", "constellate") == 0
    out = p.read_text()
    assert out.count("**Status:** Shaped") == 1     # only the strip
    assert "`**Status:** Cooking`" in out           # mid-prose untouched
    assert "**Status:** Parked" in out              # code-fence line untouched


def test_atomic_write_leaves_no_temp(tmp_path, monkeypatch):
    d = _ideas(tmp_path)
    _idea(d, "idea-foo.md",
          {"id": "idea-foo", "type": "idea", "status": "open", "tags": "[idea]"},
          "# Foo\n\nspark")
    _patch_vault(monkeypatch, tmp_path)
    plan.shape("foo", "todo")
    assert not list(d.glob(".plan-*.tmp"))


# --- idea resolution ---------------------------------------------------------

def test_no_match_returns_1(tmp_path, monkeypatch, capsys):
    _ideas(tmp_path)
    _patch_vault(monkeypatch, tmp_path)
    assert plan.shape("nope", "constellate") == 1
    assert "no idea matches" in capsys.readouterr().out


def test_ambiguous_lists_candidates(tmp_path, monkeypatch, capsys):
    d = _ideas(tmp_path)
    _idea(d, "idea-feed-one.md", {"id": "1", "status": "open"}, "# Feed One")
    _idea(d, "idea-feed-two.md", {"id": "2", "status": "open"}, "# Feed Two")
    _patch_vault(monkeypatch, tmp_path)
    assert plan.shape("feed", "constellate") == 1
    out = capsys.readouterr().out
    assert "ambiguous" in out
    assert "idea-feed-one" in out and "idea-feed-two" in out


def test_exact_stem_beats_substring(tmp_path, monkeypatch):
    d = _ideas(tmp_path)
    exact = _idea(d, "idea-feed.md", {"id": "1", "status": "open"}, "# Feed")
    _idea(d, "idea-feed-extra.md", {"id": "2", "status": "open"}, "# Feed Extra")
    _patch_vault(monkeypatch, tmp_path)
    # 'feed' resolves to the exact stem (idea-feed), not ambiguous
    assert plan.shape("feed", "todo") == 0
    assert "project: todo" in exact.read_text()


# --- downstream: authoritative project: key ----------------------------------

def test_planned_idea_matches_only_its_project(tmp_path, monkeypatch):
    d = _ideas(tmp_path)
    _idea(d, "idea-foo.md",
          {"id": "idea-foo", "type": "idea", "status": "open", "tags": "[idea, constellate]"},
          "# Foo\n\nmentions todoist and [[01 Projects/todo]]")
    _patch_vault(monkeypatch, tmp_path)
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)

    plan.shape("foo", "constellate")
    # now declares project: constellate — authoritative
    planned, backlog_items = backlog._obsidian_items("constellate")
    assert [i.title for i in planned] == ["Foo"]
    # must NOT fuzzy-match 'todo' even though 'todoist' + [[…/todo]] appear
    assert backlog._obsidian_items("todo") == ([], [])


# --- execution plan records --------------------------------------------------

def test_create_execution_plan_writes_shaped_backlog_record(tmp_path, monkeypatch):
    plan_file = tmp_path / "plan.md"
    plan_file.write_text("## Steps\n\n- Write tests first.\n", encoding="utf-8")
    _patch_vault(monkeypatch, tmp_path, projects=("cockpit",))

    assert plan.create_execution_plan(
        plan_id="agentic-flow",
        title="Unified agentic flow",
        summary="make todo own backlog",
        project="cockpit",
        priority="high",
        plan_file=str(plan_file),
        tags=["agentic", "tests"],
        drive_query="Unified agentic flow",
        created="2026-06-03T12:00:00-04:00",
    ) == 0

    note = tmp_path / "06 Backlog" / "agentic-flow.md"
    out = note.read_text(encoding="utf-8")
    assert "id: agentic-flow" in out
    assert "type: plan" in out
    assert "status: shaped" in out
    assert "executed: false" in out
    assert "project: cockpit" in out
    assert "priority: high" in out
    assert "drive_lookup_url: https://drive.google.com/drive/search?q=Unified+agentic+flow" in out
    assert "Write tests first." in out

    index = tmp_path / "06 Backlog" / "_index.md"
    assert "[[agentic-flow]]" in index.read_text(encoding="utf-8")


def test_execution_plan_appears_in_backlog_planned_then_done_history(tmp_path, monkeypatch, capsys):
    plan_file = tmp_path / "plan.md"
    plan_file.write_text("Fixture plan body.", encoding="utf-8")
    _patch_vault(monkeypatch, tmp_path, projects=("cockpit",))
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(backlog, "load_all", lambda: [])

    plan.create_execution_plan(
        plan_id="agentic-flow",
        title="Unified agentic flow",
        summary="make todo own backlog",
        project="cockpit",
        plan_file=str(plan_file),
    )

    assert backlog.run("cockpit", offline=True) == 0
    out = capsys.readouterr().out
    assert "Planned  (1)" in out
    assert "Unified agentic flow" in out
    assert "Backlog / Ideas  (0)" in out

    assert plan.execute_plan(
        "agentic-flow",
        summary="Implemented with tests.",
        executed_at="2026-06-03T12:30:00-04:00",
        google_drive_url="https://drive.google.com/file/d/example",
    ) == 0

    assert backlog.run("cockpit", offline=True) == 0
    assert "Unified agentic flow" not in capsys.readouterr().out

    assert backlog.run("cockpit", offline=True, history=True) == 0
    out = capsys.readouterr().out
    assert "Done / History  (1)" in out
    assert "Unified agentic flow" in out


def test_backlog_json_includes_stable_done_group(tmp_path, monkeypatch, capsys):
    plan_file = tmp_path / "plan.md"
    plan_file.write_text("Fixture plan body.", encoding="utf-8")
    _patch_vault(monkeypatch, tmp_path, projects=("cockpit",))
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(backlog, "load_all", lambda: [])

    plan.create_execution_plan(
        plan_id="agentic-flow",
        title="Unified agentic flow",
        summary="make todo own backlog",
        project="cockpit",
        plan_file=str(plan_file),
    )
    plan.execute_plan(
        "agentic-flow",
        summary="Implemented with tests.",
        executed_at="2026-06-03T12:30:00-04:00",
    )
    capsys.readouterr()

    assert backlog.run("cockpit", offline=True, json_output=True) == 0
    data = json.loads(capsys.readouterr().out)
    assert set(data) >= {"project", "in_flight", "planned", "backlog", "done"}
    assert data["project"] == "cockpit"
    assert data["planned"] == []
    assert data["backlog"] == []
    assert data["done"][0]["title"] == "Unified agentic flow"
    assert data["done"][0]["status"] == "done"
