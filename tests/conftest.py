"""Test fixtures: every test runs against an isolated tmp store, never ~/.todo."""
from __future__ import annotations

import pytest

from todo_cli import storage


@pytest.fixture(autouse=True)
def _isolate_store(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "TODO_DIR", tmp_path)
    monkeypatch.setattr(storage, "TODOS_FILE", tmp_path / "todos.jsonl")
    monkeypatch.setattr(storage, "LOG_FILE", tmp_path / "todo.log")


@pytest.fixture(autouse=True)
def _no_live_linear(monkeypatch):
    """Never let a test reach the real Linear API or the login keychain.

    A fake key satisfies `linear.available()` without touching the keychain, and any
    unmocked HTTP call fails loudly. Tests that need transport mock `linear._graphql`
    or `linear.urllib.request.urlopen` themselves (test_linear.py).
    """
    from todo_cli import linear

    monkeypatch.setenv("TODO_LINEAR_API_KEY", "test-key-never-real")

    def _blocked(*args, **kwargs):
        raise AssertionError("test tried to reach the network (Linear); mock linear._graphql")

    monkeypatch.setattr(linear.urllib.request, "urlopen", _blocked)


@pytest.fixture
def store(tmp_path):
    return tmp_path / "todos.jsonl"
