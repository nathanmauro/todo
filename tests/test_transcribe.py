"""Unit tests for todo_cli.transcribe and the `todo transcribe` CLI verb.

All subprocess calls are mocked — no real whisper or ffmpeg is invoked.
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

from todo_cli import transcribe as tr
from todo_cli import commands, obsidian


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_audio(tmp_path: Path, name: str = "test.m4a", mtime: float | None = None) -> Path:
    audio = tmp_path / name
    audio.write_bytes(b"FAKEAUDIO")
    if mtime is not None:
        import os
        os.utime(str(audio), (mtime, mtime))
    return audio


# ---------------------------------------------------------------------------
# audio_duration
# ---------------------------------------------------------------------------

def test_audio_duration_parses_float(tmp_path):
    audio = _make_audio(tmp_path)
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="123.45\n", returncode=0)
        result = tr.audio_duration(audio)
    assert result == pytest.approx(123.45)
    args = mock_run.call_args[0][0]
    assert "ffprobe" in args[0]
    assert str(audio) in args


def test_audio_duration_returns_none_on_failure(tmp_path):
    audio = _make_audio(tmp_path)
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "ffprobe")):
        result = tr.audio_duration(audio)
    assert result is None


# ---------------------------------------------------------------------------
# select_model
# ---------------------------------------------------------------------------

def test_select_model_override_wins(tmp_path):
    audio = _make_audio(tmp_path)
    result = tr.select_model(audio, model_override="/custom/model.bin")
    assert result == "/custom/model.bin"


def test_select_model_defaults_to_base_for_short_audio(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "/base.bin")
    with patch.object(tr, "audio_duration", return_value=60.0):
        result = tr.select_model(audio)
    assert result == "/base.bin"


def test_select_model_upgrades_to_small_for_long_audio(tmp_path, monkeypatch, tmp_path_factory):
    audio = _make_audio(tmp_path)
    models = tmp_path_factory.mktemp("models")
    fake_base = models / "ggml-base.en.bin"
    fake_base.write_bytes(b"base")
    fake_small = models / "ggml-small.en.bin"
    fake_small.write_bytes(b"small")
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", str(fake_base))
    monkeypatch.setattr(tr, "_SMALL_MODEL", str(fake_small))
    with patch.object(tr, "audio_duration", return_value=700.0):  # >600s
        result = tr.select_model(audio)
    assert result == str(fake_small)


def test_select_model_stays_on_base_if_small_absent(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "/base.bin")
    monkeypatch.setattr(tr, "_SMALL_MODEL", "/nonexistent/small.bin")
    with patch.object(tr, "audio_duration", return_value=700.0):
        result = tr.select_model(audio)
    assert result == "/base.bin"


def test_select_model_returns_empty_when_no_model_configured(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "")
    result = tr.select_model(audio)
    assert result == ""


# ---------------------------------------------------------------------------
# transcribe()
# ---------------------------------------------------------------------------

def _ffmpeg_ok():
    return MagicMock(returncode=0, stdout=b"", stderr=b"")


def _whisper_ok(text: str = "hello world"):
    return MagicMock(returncode=0, stdout=text, stderr="")


def test_transcribe_returns_none_when_no_model(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "")
    result = tr.transcribe(audio)
    assert result is None


def test_transcribe_returns_text(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "/base.bin")

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        # whisper
        return _whisper_ok("this is a test transcript")

    with patch("subprocess.run", side_effect=fake_run):
        result = tr.transcribe(audio, model="/base.bin")
    assert result == "this is a test transcript"


def test_transcribe_normalises_whitespace(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        return _whisper_ok("  word1  \n word2\t word3  ")

    with patch("subprocess.run", side_effect=fake_run):
        result = tr.transcribe(audio, model="/base.bin")
    assert result == "word1 word2 word3"


def test_transcribe_returns_none_on_ffmpeg_error(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)

    with patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "ffmpeg"),
    ):
        result = tr.transcribe(audio, model="/base.bin")
    assert result is None


def test_transcribe_writes_srt_when_requested(tmp_path, monkeypatch):
    audio = _make_audio(tmp_path)
    srt_dest = tmp_path / "out.srt"

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        # whisper with -osrt: write a fake .srt next to the -of stem
        of_index = cmd.index("-of") if "-of" in cmd else None
        if of_index is not None:
            of_stem = Path(cmd[of_index + 1])
            srt_candidate = of_stem.with_name(of_stem.name + ".srt")
            srt_candidate.write_text("1\n00:00:00,000 --> 00:00:01,000\nhello\n")
        return _whisper_ok("hello")

    with patch("subprocess.run", side_effect=fake_run):
        result = tr.transcribe(audio, model="/base.bin", srt_dest=srt_dest)

    assert result == "hello"
    assert srt_dest.exists()
    assert "hello" in srt_dest.read_text()


def test_transcribe_srt_absent_does_not_raise(tmp_path, monkeypatch):
    """If whisper does not produce .srt, transcribe() still returns the text."""
    audio = _make_audio(tmp_path)
    srt_dest = tmp_path / "out.srt"

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        return _whisper_ok("words")  # no .srt file created

    with patch("subprocess.run", side_effect=fake_run):
        result = tr.transcribe(audio, model="/base.bin", srt_dest=srt_dest)

    assert result == "words"
    assert not srt_dest.exists()


# ---------------------------------------------------------------------------
# write_transcript_capture()
# ---------------------------------------------------------------------------

def test_write_transcript_capture_creates_file(tmp_path):
    audio = _make_audio(tmp_path, "voice.m4a", mtime=1_780_000_000.0)
    dest = tmp_path / "dest"
    path = tr.write_transcript_capture(audio, "hello world", dest)

    assert path.exists()
    assert path.parent == dest
    text = path.read_text()
    assert "source: transcribe" in text
    assert "type: note" in text
    assert "tags: [voice]" in text
    assert "audio: voice.m4a" in text
    assert "hello world" in text


def test_write_transcript_capture_filename_pattern(tmp_path):
    audio = _make_audio(tmp_path)
    dest = tmp_path / "dest"
    path = tr.write_transcript_capture(audio, "x", dest)
    parts = path.stem.split("-")
    assert parts[0].isdigit() and len(parts[0]) == 6  # HHMMSS
    assert parts[1] == "transcribe"
    assert len(parts[2]) == 8  # id8 hex


def test_write_transcript_capture_uses_audio_mtime(tmp_path):
    # 2024-01-15 12:34:56 UTC
    fixed_ts = 1705322096.0
    audio = _make_audio(tmp_path, "voice.m4a", mtime=fixed_ts)
    dest = tmp_path / "dest"
    path = tr.write_transcript_capture(audio, "words", dest)
    text = path.read_text()
    assert "created: 2024-01-15" in text


# ---------------------------------------------------------------------------
# cmd_transcribe (CLI verb)
# ---------------------------------------------------------------------------

@pytest.fixture
def vault(tmp_path, monkeypatch):
    monkeypatch.setattr(obsidian, "OBSIDIAN_VAULT", tmp_path)
    monkeypatch.setattr(tr, "OBSIDIAN_VAULT", tmp_path)
    return tmp_path


def _transcribe_args(**kwargs) -> argparse.Namespace:
    defaults = {"files": [], "dest": None, "model": None, "srt": False}
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def test_cmd_transcribe_missing_file_returns_nonzero(vault, capsys):
    args = _transcribe_args(files=["/nonexistent/audio.m4a"])
    rc = commands.cmd_transcribe(args)
    assert rc != 0
    err = capsys.readouterr().err
    assert "not found" in err


def test_cmd_transcribe_no_model_returns_nonzero(tmp_path, vault, monkeypatch, capsys):
    audio = _make_audio(tmp_path, "voice.m4a")
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "")
    args = _transcribe_args(files=[str(audio)])
    rc = commands.cmd_transcribe(args)
    assert rc != 0


def test_cmd_transcribe_writes_capture_file(tmp_path, vault, monkeypatch):
    audio = _make_audio(tmp_path, "voice.m4a")
    dest = tmp_path / "out"
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "/base.bin")

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        return _whisper_ok("the transcript text")

    with patch("subprocess.run", side_effect=fake_run):
        with patch.object(tr, "audio_duration", return_value=30.0):
            args = _transcribe_args(files=[str(audio)], dest=str(dest))
            rc = commands.cmd_transcribe(args)

    assert rc == 0
    md_files = list(dest.glob("*.md"))
    assert len(md_files) == 1
    content = md_files[0].read_text()
    assert "source: transcribe" in content
    assert "the transcript text" in content
    assert "audio: voice.m4a" in content


def test_cmd_transcribe_multiple_files(tmp_path, vault, monkeypatch):
    a1 = _make_audio(tmp_path, "a1.m4a")
    a2 = _make_audio(tmp_path, "a2.m4a")
    dest = tmp_path / "out"
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "/base.bin")

    call_count = {"n": 0}

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        call_count["n"] += 1
        return _whisper_ok(f"transcript {call_count['n']}")

    with patch("subprocess.run", side_effect=fake_run):
        with patch.object(tr, "audio_duration", return_value=30.0):
            args = _transcribe_args(files=[str(a1), str(a2)], dest=str(dest))
            rc = commands.cmd_transcribe(args)

    assert rc == 0
    assert len(list(dest.glob("*.md"))) == 2


def test_cmd_transcribe_uses_default_dest(tmp_path, vault, monkeypatch):
    audio = _make_audio(tmp_path, "voice.m4a")
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "/base.bin")

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        return _whisper_ok("words")

    with patch("subprocess.run", side_effect=fake_run):
        with patch.object(tr, "audio_duration", return_value=30.0):
            args = _transcribe_args(files=[str(audio)])
            rc = commands.cmd_transcribe(args)

    assert rc == 0
    # default dest = <vault>/captures/YYYY-MM-DD/ (today)
    import datetime as dt

    today_dir = vault / "captures" / dt.date.today().isoformat()
    assert any(today_dir.glob("*.md"))


def test_cmd_transcribe_srt_flag(tmp_path, vault, monkeypatch, capsys):
    audio = _make_audio(tmp_path, "voice.m4a")
    dest = tmp_path / "out"
    monkeypatch.setattr(tr, "_DEFAULT_MODEL", "/base.bin")

    def fake_run(cmd, **kwargs):
        if "ffmpeg" in cmd[0]:
            return _ffmpeg_ok()
        # write a fake .srt when requested
        if "-osrt" in cmd:
            of_index = cmd.index("-of")
            of_stem = Path(cmd[of_index + 1])
            (of_stem.with_name(of_stem.name + ".srt")).write_text("1\n00:00,000\nhello\n")
        return _whisper_ok("hello")

    with patch("subprocess.run", side_effect=fake_run):
        with patch.object(tr, "audio_duration", return_value=30.0):
            args = _transcribe_args(files=[str(audio)], dest=str(dest), srt=True)
            rc = commands.cmd_transcribe(args)

    assert rc == 0
    out = capsys.readouterr().out
    assert "srt" in out.lower() or any(dest.glob("*.srt"))
