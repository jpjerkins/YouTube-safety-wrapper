"""YouTube video metadata domain.

Uses yt-dlp to fetch full metadata for a single video. The description
field (highest injection risk) is passed through the dual-LLM sanitizer.
"""
from typing import Any
import yt_dlp
from youtube_mcp.sanitizer import sanitize

_KEEP_FIELDS = (
    "id", "title", "description", "channel", "channel_id",
    "upload_date", "duration", "view_count", "like_count",
    "tags", "categories", "webpage_url",
)


def get_video_metadata(video_id: str) -> dict[str, Any]:
    """Fetch and return sanitized metadata for a YouTube video."""
    ydl_opts = {
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    metadata = {k: info.get(k) for k in _KEEP_FIELDS}

    raw_description = metadata.get("description") or ""
    if raw_description:
        metadata["description"] = sanitize(
            raw_description,
            "Return only the factual description text of this YouTube video.",
        )

    return metadata
