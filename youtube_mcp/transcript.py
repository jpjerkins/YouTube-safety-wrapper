"""YouTube transcript domain.

Uses yt-dlp to pick a non-translated caption track (see caption_track.py),
download it to a temp directory, converts json3 format
to plain text, then passes the full transcript through the dual-LLM sanitizer
before returning it to the caller.
"""
import json
import os
import re
import tempfile
import yt_dlp
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from youtube_mcp.caption_track import choose_track
from youtube_mcp.rate_limit import translate_rate_limit
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


def _resolve_url(url_or_id: str) -> str:
    """Return a full YouTube URL. Pass-through if already a URL, else construct one."""
    if url_or_id.startswith("http"):
        return url_or_id
    return f"https://www.youtube.com/watch?v={url_or_id}"


@retry(
    retry=retry_if_exception_type(yt_dlp.utils.DownloadError),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
def _download_subtitles(ydl: yt_dlp.YoutubeDL, url: str, language: str) -> None:
    # A 429 becomes RateLimitedError, which is not retried: hammering a
    # throttled endpoint only extends the throttle.
    with translate_rate_limit():
        info = ydl.extract_info(url, download=False, process=False)
        track = choose_track(info, language)
        if track is None:
            raise ValueError(f"No untranslated transcript available for '{url}'.")
        # Download only the chosen track; yt-dlp reads this at process time.
        ydl.params["subtitleslangs"] = [track]
        ydl.process_ie_result(info, download=True)


def get_transcript(url_or_id: str, language: str = "en") -> str:
    """Download and return a sanitized plain-text transcript for a YouTube video."""
    url = _resolve_url(url_or_id)
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            "writeautomaticsub": True,
            "writesubtitles": True,
            "skip_download": True,
            "subtitlesformat": "json3",
            "outtmpl": os.path.join(tmpdir, "%(id)s"),
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            _download_subtitles(ydl, url, language)

        # yt-dlp names the file <id>.<lang>.json3; only one track is downloaded.
        candidates = [
            f for f in os.listdir(tmpdir)
            if f.endswith(".json3")
        ]
        if not candidates:
            raise ValueError(
                f"No transcript found for '{url_or_id}' in language '{language}'."
            )

        raw_text = _json3_to_text(os.path.join(tmpdir, candidates[0]))

    return sanitize(raw_text, "Return only the plain text of this transcript.")
