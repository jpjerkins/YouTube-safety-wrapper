"""Tests for the dual-LLM sanitizer's handling of empty model output."""
import pytest
from unittest.mock import MagicMock

from youtube_mcp import sanitizer


def _mock_response(content, finish_reason="stop"):
    choice = MagicMock()
    choice.message.content = content
    choice.finish_reason = finish_reason
    response = MagicMock()
    response.choices = [choice]
    return response


def test_sanitize_returns_content_on_success(monkeypatch):
    monkeypatch.setattr(
        sanitizer._client.chat.completions,
        "create",
        MagicMock(return_value=_mock_response("cleaned text")),
    )
    assert sanitizer.sanitize("raw", "task") == "cleaned text"


def test_sanitize_raises_when_model_returns_no_content(monkeypatch):
    monkeypatch.setattr(
        sanitizer._client.chat.completions,
        "create",
        MagicMock(return_value=_mock_response(None, finish_reason="content_filter")),
    )
    with pytest.raises(RuntimeError, match="content_filter"):
        sanitizer.sanitize("raw", "task")
