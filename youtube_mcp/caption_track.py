"""Caption track selection.

YouTube labels each video's original speech-recognition track "<lang>-orig".
Other auto-caption languages (often including plain "en") are machine
translations, which YouTube rate-limits (HTTP 429) aggressively. So we only
ever pick a track that is either human-made or in the video's original
language, and let the downstream LLM handle any translation.
"""
from typing import Any, Optional

# yt-dlp lists livestream chat replay as a "subtitle"; it is not a transcript.
_NOT_TRANSCRIPTS = {"live_chat"}


def choose_track(info: dict[str, Any], language: str) -> Optional[str]:
    """Return the best non-translated caption language code, or None.

    Order: manual subs in `language`, original auto captions in `language`,
    original auto captions in any language, then manual subs in any language.
    """
    manual = {
        code: track for code, track in (info.get("subtitles") or {}).items()
        if code not in _NOT_TRANSCRIPTS
    }
    auto = info.get("automatic_captions") or {}

    if language in manual:
        return language
    if f"{language}-orig" in auto:
        return f"{language}-orig"
    for code in auto:
        if code.endswith("-orig"):
            return code
    return next(iter(manual), None)
