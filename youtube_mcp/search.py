"""YouTube search domain.

Uses yt-dlp to search YouTube and returns sanitized results.
Free-text fields (title, channel) are passed through the dual-LLM sanitizer
before being returned to the caller.
"""
from typing import Any
import yt_dlp
from youtube_mcp.sanitizer import sanitize


def search_youtube(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Search YouTube and return a list of video summaries."""
    ydl_opts = {
        "extract_flat": "in_playlist",
        "quiet": True,
        "no_warnings": True,
    }

    url = f"ytsearch{max_results}:{query}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    results = []
    for entry in info.get("entries") or []:
        raw_title = entry.get("title") or ""
        raw_channel = entry.get("channel") or entry.get("uploader") or ""

        results.append(
            {
                "id": entry.get("id"),
                "title": sanitize(raw_title, "Return only the video title text."),
                "channel": sanitize(raw_channel, "Return only the channel name."),
                "duration_seconds": entry.get("duration"),
                "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry.get('id')}",
            }
        )

    return results
