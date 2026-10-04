"""Tests for choosing which caption track to download."""
from youtube_mcp.caption_track import choose_track


def _info(subtitles=None, automatic_captions=None):
    return {"subtitles": subtitles or {}, "automatic_captions": automatic_captions or {}}


def test_prefers_manual_subtitles_in_requested_language():
    info = _info(subtitles={"en": []}, automatic_captions={"en-orig": [], "en": []})
    assert choose_track(info, "en") == "en"


def test_uses_original_auto_captions_in_requested_language():
    info = _info(automatic_captions={"en-orig": [], "en": [], "fr": []})
    assert choose_track(info, "en") == "en-orig"


def test_falls_back_to_original_language_rather_than_translation():
    # Bangla video: plain "en" here is a machine translation YouTube throttles.
    info = _info(automatic_captions={"bn-orig": [], "bn": [], "en": [], "fr": []})
    assert choose_track(info, "en") == "bn-orig"


def test_falls_back_to_any_manual_subtitles():
    info = _info(subtitles={"de": []}, automatic_captions={"en": [], "de-en": []})
    assert choose_track(info, "en") == "de"


def test_returns_none_when_only_translations_exist():
    info = _info(automatic_captions={"en": [], "fr": []})
    assert choose_track(info, "en") is None


def test_handles_missing_caption_keys():
    assert choose_track({}, "en") is None


def test_ignores_live_chat_pseudo_subtitles():
    info = _info(subtitles={"live_chat": []}, automatic_captions={"en": []})
    assert choose_track(info, "en") is None
