"""YouTube transcript domain.

Uses yt-dlp to download subtitles to a temp directory, converts json3 format
to plain text, then passes the full transcript through the dual-LLM sanitizer
before returning it to the caller.
"""
import json
import os
import re
import tempfile
import yt_dlp
from youtube_mcp.sanitizer import sanitize


def _json3_to_text(path: str) -> str:
    """Convert a yt-dlp json3 subtitle file to plain text."""
    with open(path) as f:
        data = json.load(f)

    parts = []
    for event in data.get("events", []):
        for seg in event.get("segs", []):
            text = seg.get("utf8", "")
            text = re.sub(r"<[^>]+>", "", text)  # strip HTML tags
            parts.append(text)

    return re.sub(r"\s+", " ", "".join(parts)).strip()


def get_transcript(video_id: str, language: str = "en") -> str:
    """Download and return a sanitized plain-text transcript for a YouTube video."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            "writeautomaticsub": True,
            "writesubtitles": True,
            "skip_download": True,
            "subtitleslangs": [language],
            "subtitlesformat": "json3",
            "outtmpl": os.path.join(tmpdir, "%(id)s"),
            "quiet": True,
            "no_warnings": True,
        }

        url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # yt-dlp names the file: <id>.<lang>.json3 or <id>.<lang>-auto.json3
        candidates = [
            f for f in os.listdir(tmpdir)
            if f.endswith(".json3")
        ]
        if not candidates:
            raise ValueError(
                f"No transcript found for video '{video_id}' in language '{language}'."
            )

        raw_text = _json3_to_text(os.path.join(tmpdir, candidates[0]))

    return sanitize(raw_text, "Return only the plain text of this transcript.")
