"""`todo backlog` — per-project pull across Obsidian + Todoist.

Pins the load-bearing behavior: how a note is matched to a project (the
`project:` key wins over fuzzy signals), how Todoist lanes classify into
in-flight / planned / ideas, and the `--if-project` guard that keeps a global
SessionStart hook silent unless the cwd is a known project.
"""
from __future__ import annotations

import todo_cli.backlog as backlog
from todo_cli.models import TodoEntry, TodoistSync


# --- fixtures ----------------------------------------------------------------

def _vault(tmp_path):
    ideas = tmp_path / "05 Notes" / "ideas"
    bl = tmp_path / "06 Backlog"
    ideas.mkdir(parents=True)
    bl.mkdir(parents=True)
    return ideas, bl


def _write(folder, name, frontmatter, body):
    fm = "".join(f"{k}: {v}\n" for k, v in frontmatter.items())
    folder.joinpath(name).write_text(f"---\n{fm}---\n\n{body}\n")


def _patch_structure(monkeypatch, projects=("constellate", "todo")):
    monkeypatch.setattr(backlog, "taxonomy_labels", lambda: {"projects": list(projects)})
    monkeypatch.setattr(backlog, "project_role_ids", lambda: {
        "inbox": "INBOX", "current_work": "CW", "idea_cooker": "IC",
        "resource": "RES", "archive": "ARCH",
    })
    monkeypatch.setattr(backlog, "idea_cooker_sections", lambda: {
        "dreamer": "D", "cooking": "C", "shaped": "S", "board_ready": "BR", "parked": "P",
    })


# --- _match_project priority -------------------------------------------------

def test_match_project_key_wins():
    assert backlog._match_project(
        "constellate", "idea-x", {"project": "constellate"}, "no mention"
    ) == "project:"


def test_match_tag():
    assert backlog._match_project(
        "constellate", "idea-x", {"tags": "[idea, constellate]"}, "body"
    ) == "tag"


def test_match_wikilink():
    assert backlog._match_project(
        "constellate", "idea-x", {}, "see [[01 Projects/constellate]] here"
    ) == "wikilink"


def test_match_prose():
    assert backlog._match_project(
        "constellate", "idea-x", {}, "- Projects: constellate, foo"
    ) == "prose"


def test_match_filename():
    assert backlog._match_project(
        "constellate", "constellate-redesign", {}, "nothing"
    ) == "filename"


def test_no_match():
    assert backlog._match_project(
        "constellate", "idea-x", {"tags": "[idea]"}, "unrelated"
    ) is None


# --- Obsidian planned vs backlog split ---------------------------------------

def test_obsidian_planned_vs_backlog(tmp_path, monkeypatch):
    ideas, bl = _vault(tmp_path)
    _patch_structure(monkeypatch)
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)
    _write(ideas, "idea-a.md",
           {"type": "idea", "status": "shaped", "project": "constellate", "tags": "[idea]"},
           "# Idea A\nbody")
    _write(bl, "b.md",
           {"type": "backlog", "status": "open", "priority": "med", "project": "constellate", "tags": "[backlog]"},
           "# Backlog B\nbody")
    planned, back = backlog._obsidian_items("constellate")
    assert [i.title for i in planned] == ["Idea A"]
    assert [i.title for i in back] == ["Backlog B"]
    assert back[0].priority == "med"


# --- --if-project guard ------------------------------------------------------

def test_if_project_silent_for_unknown(tmp_path, monkeypatch, capsys):
    _vault(tmp_path)
    _patch_structure(monkeypatch, projects=("constellate",))
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(backlog, "load_all", lambda: [])
    assert backlog.run("idea-hub", if_project=True) == 0
    assert capsys.readouterr().out == ""


def test_if_project_silent_when_empty(tmp_path, monkeypatch, capsys):
    _vault(tmp_path)
    _patch_structure(monkeypatch, projects=("constellate",))
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(backlog, "load_all", lambda: [])
    assert backlog.run("constellate", if_project=True) == 0
    assert capsys.readouterr().out == ""


def test_if_project_prints_when_present(tmp_path, monkeypatch, capsys):
    _, bl = _vault(tmp_path)
    _patch_structure(monkeypatch, projects=("constellate",))
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(backlog, "load_all", lambda: [])
    _write(bl, "b.md",
           {"type": "backlog", "status": "open", "project": "constellate", "tags": "[x]"},
           "# Backlog B\nx")
    backlog.run("constellate", if_project=True)
    out = capsys.readouterr().out
    assert "constellate" in out
    assert "Backlog / Ideas" in out
    assert "Backlog B" in out


# --- Todoist classification --------------------------------------------------

def test_live_classification(tmp_path, monkeypatch, capsys):
    _vault(tmp_path)
    _patch_structure(monkeypatch, projects=("constellate",))
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(backlog.todoist, "token", lambda: "tok")
    tasks = [
        {"id": "1", "content": "inflight task", "labels": ["constellate"], "project_id": "CW", "section_id": None},
        {"id": "2", "content": "shaped plan", "labels": ["constellate"], "project_id": "IC", "section_id": "S"},
        {"id": "3", "content": "raw idea", "labels": ["constellate"], "project_id": "IC", "section_id": "D"},
        {"id": "4", "content": "archived", "labels": ["constellate"], "project_id": "ARCH", "section_id": None},
        {"id": "5", "content": "other proj", "labels": ["something-else"], "project_id": "CW", "section_id": None},
    ]
    monkeypatch.setattr(backlog.todoist, "list_active_tasks", lambda tok: tasks)
    backlog.run("constellate")
    out = capsys.readouterr().out
    assert "In flight  (1)" in out and "inflight task" in out
    assert "Planned  (1)" in out and "shaped plan" in out
    assert "raw idea" in out          # Idea Cooker / Dreamer -> backlog/ideas
    assert "archived" not in out      # resource/archive lanes skipped
    assert "other proj" not in out    # not labeled constellate


def test_offline_mirror_classification(tmp_path, monkeypatch, capsys):
    _vault(tmp_path)
    _patch_structure(monkeypatch, projects=("constellate",))
    monkeypatch.setattr(backlog, "OBSIDIAN_VAULT", tmp_path)

    def mk(text, pid, project="constellate"):
        e = TodoEntry(text=text, project=project, status="open")
        e.sync.todoist = TodoistSync(task_id="t", ts="x", project_id=pid)
        return e

    entries = [
        mk("cw task", "CW"),
        mk("ic task", "IC"),
        mk("inbox task", "INBOX"),
        mk("other proj", "CW", project="elsewhere"),
    ]
    monkeypatch.setattr(backlog, "load_all", lambda: entries)
    backlog.run("constellate", offline=True)
    out = capsys.readouterr().out
    assert "cw task" in out          # current_work -> in flight
    assert "ic task" in out          # idea_cooker -> planned
    assert "inbox task" in out       # inbox -> backlog/ideas
    assert "other proj" not in out   # different project label filtered out
