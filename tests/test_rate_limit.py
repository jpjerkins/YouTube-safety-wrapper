"""Tests for YouTube rate-limit detection."""
from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

from youtube_mcp.rate_limit import RateLimitedError, translate_rate_limit
from youtube_mcp.transcript import _download_subtitles
from youtube_mcp.metadata import get_video_metadata

_429 = "ERROR: Unable to download video subtitles for 'en': HTTP Error 429: Too Many Requests"


def test_translate_rate_limit_converts_429_download_error():
    with pytest.raises(RateLimitedError):
        with translate_rate_limit():
            raise yt_dlp.utils.DownloadError(_429)


def test_translate_rate_limit_passes_other_download_errors_through():
    with pytest.raises(yt_dlp.utils.DownloadError):
        with translate_rate_limit():
            raise yt_dlp.utils.DownloadError("ERROR: something else")


def test_rate_limited_error_message_explains_what_to_do():
    msg = str(RateLimitedError())
    assert "rate-limiting" in msg
    assert "429" in msg
    assert "try again" in msg


def test_download_subtitles_does_not_retry_on_429():
    ydl = MagicMock()
    ydl.download.side_effect = yt_dlp.utils.DownloadError(_429)

    with pytest.raises(RateLimitedError):
        _download_subtitles(ydl, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    assert ydl.download.call_count == 1


def test_get_video_metadata_raises_rate_limited_on_429():
    ydl = MagicMock()
    ydl.__enter__.return_value = ydl
    ydl.extract_info.side_effect = yt_dlp.utils.DownloadError("HTTP Error 429: Too Many Requests")
    with patch("youtube_mcp.metadata.yt_dlp.YoutubeDL", return_value=ydl):
        with pytest.raises(RateLimitedError):
            get_video_metadata("dQw4w9WgXcQ")
