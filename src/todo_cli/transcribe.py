"""Audio transcription helpers: ffmpeg re-encode + whisper.cpp inference.

Shared by the Telegram voice-note pipeline (telegram.py) and the CLI
`todo transcribe` verb (commands.py). The Telegram path is a pure refactor —
no behaviour change. The CLI verb adds file-mtime-as-created, model auto-
selection, and optional SRT output.
"""
from __future__ import annotations

import datetime as dt
import os
import re
import secrets
import subprocess
import tempfile
from pathlib import Path

from .config import OBSIDIAN_VAULT, WHISPER_BIN, WHISPER_MODEL
from .storage import log

# Default model (may be overridden per call)
_DEFAULT_MODEL = WHISPER_MODEL

# The small.en model path — auto-selected for long recordings when present
_SMALL_MODEL = str(Path.home() / ".cache" / "whisper" / "ggml-small.en.bin")

# Duration threshold (seconds) for auto-switching to small.en
_LONG_AUDIO_SECS = 600.0  # 10 minutes

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def audio_duration(audio: Path) -> float | None:
    """Return audio duration in seconds via ffprobe, or None on failure."""
    try:
        r = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                str(audio),
            ],
            capture_output=True, text=True, check=True,
        )
        return float(r.stdout.strip())
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError) as exc:
        log(f"transcribe: ffprobe failed for {audio}: {exc}")
        return None


def select_model(audio: Path, model_override: str | None = None) -> str:
    """Choose the whisper model for this audio file.

    Priority:
      1. Explicit --model override.
      2. Auto-upgrade to small.en when the recording is longer than
         _LONG_AUDIO_SECS AND the small model exists.
      3. Default (WHISPER_MODEL from config / env).

    Never downloads a model — if small.en is absent, falls back to base.
    """
    if model_override:
        return model_override
    if _DEFAULT_MODEL and Path(_DEFAULT_MODEL).exists():
        dur = audio_duration(audio)
        if dur is not None and dur > _LONG_AUDIO_SECS:
            if Path(_SMALL_MODEL).exists():
                log(f"transcribe: {audio.name} is {dur:.0f}s — using small.en")
                return _SMALL_MODEL
    return _DEFAULT_MODEL or ""


def transcribe(
    audio: Path,
    *,
    model: str | None = None,
    srt_dest: Path | None = None,
) -> str | None:
    """Transcribe an audio file to text; optionally write an SRT alongside.

    Args:
        audio:     Input audio (any format ffmpeg supports, including m4a/ogg).
        model:     Explicit model path. None = auto-select via select_model().
        srt_dest:  If given, write a .srt file to this exact path after
                   transcription. whisper-cli's -osrt flag is used; it writes
                   to the same stem as -of, so we use a temp stem and rename.

    Returns:
        Plain-text transcript string, or None if transcription is not
        configured (no model) or fails.
    """
    resolved_model = select_model(audio, model)
    if not resolved_model:
        return None

    # Re-encode to 16 kHz mono WAV in a temp file (whisper expects WAV)
    fd, wav_tmp = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    wav = Path(wav_tmp)

    # Temp stem for whisper -of (whisper appends .srt / .txt itself)
    fd2, of_tmp = tempfile.mkstemp()
    os.close(fd2)
    of_path = Path(of_tmp)

    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(audio),
                "-ar", "16000", "-ac", "1", "-f", "wav", str(wav),
            ],
            capture_output=True, check=True,
        )

        cmd = [
            WHISPER_BIN, "-m", resolved_model,
            "-f", str(wav),
            "-nt", "-np",
        ]
        if srt_dest is not None:
            cmd += ["-osrt", "-of", str(of_path)]

        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        text = " ".join(r.stdout.split()).strip() or None

        if srt_dest is not None:
            candidate = of_path.with_name(of_path.name + ".srt")
            if candidate.exists():
                candidate.replace(srt_dest)
            else:
                log(f"transcribe: -osrt requested but whisper produced no .srt for {audio.name}")

        return text

    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        log(f"transcribe error: {exc}")
        return None
    finally:
        wav.unlink(missing_ok=True)
        of_path.unlink(missing_ok=True)


def _slug(name: str, max_len: int = 24) -> str:
    """Derive a short lowercase slug from a filename stem."""
    raw = Path(name).stem.lower()
    slug = _SLUG_RE.sub("-", raw).strip("-")
    return slug[:max_len].strip("-") or "audio"


def default_dest() -> Path:
    """Default output directory for transcribed captures: captures/YYYY-MM-DD/."""
    today = dt.date.today().isoformat()
    return OBSIDIAN_VAULT / "captures" / today


def write_transcript_capture(
    audio: Path,
    transcript: str,
    dest_dir: Path,
) -> Path:
    """Write a single Markdown capture file for a transcribed audio file.

    Format mirrors the Telegram capture format (obsidian.py write_capture):
    YAML frontmatter (id, created, source, type, status, tags) followed by
    the transcript as the body. Uses the audio file's mtime for ``created``.
    Filename: <HHMMSS>-transcribe-<id8>.md
    """
    mtime = audio.stat().st_mtime
    created_dt = dt.datetime.fromtimestamp(mtime).astimezone()
    created = created_dt.isoformat(timespec="seconds")
    id8 = secrets.token_hex(4)

    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{created_dt.strftime('%H%M%S')}-transcribe-{id8}.md"
    path = dest_dir / filename

    frontmatter = (
        "---\n"
        f"id: {id8}\n"
        f"created: {created}\n"
        "source: transcribe\n"
        "type: note\n"
        "status: open\n"
        f"tags: [voice]\n"
        f"audio: {audio.name}\n"
        "---\n"
    )
    path.write_text(frontmatter + "\n" + transcript + "\n")
    log(f"transcribe capture -> {path}")
    return path
