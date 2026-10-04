"""Tests for transcript module URL resolution."""
from unittest.mock import MagicMock

import pytest

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


_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def _ydl(info=None):
    ydl = MagicMock()
    ydl.params = {}
    ydl.extract_info.return_value = info or {
        "subtitles": {}, "automatic_captions": {"bn-orig": [], "en": []},
    }
    return ydl


def test_download_subtitles_downloads_only_the_chosen_track():
    ydl = _ydl()

    _download_subtitles(ydl, _URL, "en")

    ydl.extract_info.assert_called_once_with(_URL, download=False, process=False)
    assert ydl.params["subtitleslangs"] == ["bn-orig"]
    ydl.process_ie_result.assert_called_once_with(ydl.extract_info.return_value, download=True)


def test_download_subtitles_raises_value_error_when_no_usable_track():
    ydl = _ydl({"subtitles": {}, "automatic_captions": {"en": []}})

    with pytest.raises(ValueError):
        _download_subtitles(ydl, _URL, "en")

    ydl.process_ie_result.assert_not_called()


def test_download_subtitles_retries_transient_download_error():
    ydl = _ydl()
    ydl.process_ie_result.side_effect = [
        yt_dlp.utils.DownloadError("transient failure"),
        yt_dlp.utils.DownloadError("transient failure"),
        None,
    ]

    _download_subtitles(ydl, _URL, "en")

    assert ydl.process_ie_result.call_count == 3


def test_download_subtitles_gives_up_after_max_attempts():
    ydl = _ydl()
    ydl.process_ie_result.side_effect = yt_dlp.utils.DownloadError("persistent failure")

    with pytest.raises(yt_dlp.utils.DownloadError):
        _download_subtitles(ydl, _URL, "en")

    assert ydl.process_ie_result.call_count == 3
