"""Tests for transcript module URL resolution."""
from unittest.mock import MagicMock

import yt_dlp

from youtube_mcp.transcript import _resolve_url, _download_subtitles


def test_resolve_url_passes_through_full_url():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert _resolve_url(url) == url


def test_resolve_url_passes_through_youtu_be():
    url = "https://youtu.be/dQw4w9WgXcQ"
    assert _resolve_url(url) == url


def test_resolve_url_constructs_url_from_bare_id():
    assert _resolve_url("dQw4w9WgXcQ") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


from youtube_mcp.metadata import _resolve_url as metadata_resolve_url


def test_metadata_resolve_url_passthrough():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert metadata_resolve_url(url) == url


def test_metadata_resolve_url_from_bare_id():
    assert metadata_resolve_url("dQw4w9WgXcQ") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_download_subtitles_retries_transient_download_error():
    ydl = MagicMock()
    ydl.download.side_effect = [
        yt_dlp.utils.DownloadError("transient failure"),
        yt_dlp.utils.DownloadError("transient failure"),
        None,
    ]

    _download_subtitles(ydl, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    assert ydl.download.call_count == 3


def test_download_subtitles_gives_up_after_max_attempts():
    ydl = MagicMock()
    ydl.download.side_effect = yt_dlp.utils.DownloadError("persistent failure")

    try:
        _download_subtitles(ydl, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert False, "expected DownloadError to be raised"
    except yt_dlp.utils.DownloadError:
        pass

    assert ydl.download.call_count == 3
