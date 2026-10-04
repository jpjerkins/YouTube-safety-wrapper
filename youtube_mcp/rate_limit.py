"""YouTube rate-limit detection.

yt-dlp reports YouTube throttling (HTTP 429) as a generic DownloadError.
This module turns that into a distinct RateLimitedError so callers can
skip pointless retries and tell the user what actually happened.
"""
from contextlib import contextmanager
from typing import Iterator

import yt_dlp


class RateLimitedError(Exception):
    """YouTube refused the request with HTTP 429 Too Many Requests."""

    def __init__(self) -> None:
        super().__init__(
            "YouTube is rate-limiting this server (HTTP 429). "
            "Wait a few hours and try again; if it keeps happening, "
            "yt-dlp in youtube-mcp may need upgrading."
        )


def _is_rate_limited(err: Exception) -> bool:
    return "HTTP Error 429" in str(err)


@contextmanager
def translate_rate_limit() -> Iterator[None]:
    """Re-raise a yt-dlp 429 DownloadError as RateLimitedError."""
    try:
        yield
    except yt_dlp.utils.DownloadError as e:
        if _is_rate_limited(e):
            raise RateLimitedError() from e
        raise
