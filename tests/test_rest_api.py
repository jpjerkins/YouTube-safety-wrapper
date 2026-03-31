"""Tests for REST API endpoints."""
from unittest.mock import patch
from fastapi.testclient import TestClient
from youtube_mcp.server import app


def test_transcript_endpoint_returns_plain_text():
    with patch("youtube_mcp.server.get_transcript", return_value="Hello world transcript."):
        client = TestClient(app)
        response = client.get("/transcript?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert response.status_code == 200
    assert response.text == "Hello world transcript."
    assert "text/plain" in response.headers["content-type"]


def test_transcript_endpoint_passes_language_param():
    with patch("youtube_mcp.server.get_transcript", return_value="Hola.") as mock_fn:
        client = TestClient(app)
        client.get("/transcript?url=https://youtu.be/dQw4w9WgXcQ&language=es")
    mock_fn.assert_called_once_with("https://youtu.be/dQw4w9WgXcQ", "es")


def test_transcript_endpoint_defaults_language_to_en():
    with patch("youtube_mcp.server.get_transcript", return_value="Hi.") as mock_fn:
        client = TestClient(app)
        client.get("/transcript?url=https://youtu.be/dQw4w9WgXcQ")
    mock_fn.assert_called_once_with("https://youtu.be/dQw4w9WgXcQ", "en")


def test_transcript_endpoint_404_when_not_found():
    with patch("youtube_mcp.server.get_transcript", side_effect=ValueError("No transcript found")):
        client = TestClient(app)
        response = client.get("/transcript?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert response.status_code == 404


def test_transcript_endpoint_missing_url_param_returns_422():
    client = TestClient(app)
    response = client.get("/transcript")
    assert response.status_code == 422
