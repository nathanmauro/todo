"""Test fixtures: every test runs against an isolated tmp store, never ~/.todo."""
from __future__ import annotations

import pytest

from todo_cli import storage


@pytest.fixture(autouse=True)
def _isolate_store(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "TODO_DIR", tmp_path)
    monkeypatch.setattr(storage, "TODOS_FILE", tmp_path / "todos.jsonl")
    monkeypatch.setattr(storage, "LOG_FILE", tmp_path / "todo.log")


@pytest.fixture
def store(tmp_path):
    return tmp_path / "todos.jsonl"
