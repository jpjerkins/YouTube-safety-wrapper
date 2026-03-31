"""Tests for transcript module URL resolution."""
from youtube_mcp.transcript import _resolve_url


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
