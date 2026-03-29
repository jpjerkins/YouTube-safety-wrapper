"""MCP tool registration.

Wires the three YouTube domain functions up as MCP tools.
"""
from mcp.server.fastmcp import FastMCP
from youtube_mcp.search import search_youtube
from youtube_mcp.metadata import get_video_metadata
from youtube_mcp.transcript import get_transcript


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def search(query: str, max_results: int = 10) -> list[dict]:
        """Search YouTube videos.

        Returns a list of results with id, title, channel, duration_seconds, url.
        All free-text fields are sanitized against prompt injection.
        """
        return search_youtube(query, max_results)

    @mcp.tool()
    def video_metadata(video_id: str) -> dict:
        """Get metadata for a YouTube video by its ID.

        Returns id, title, description, channel, upload_date, duration,
        view_count, like_count, tags, categories, webpage_url.
        The description is sanitized against prompt injection.
        """
        return get_video_metadata(video_id)

    @mcp.tool()
    def transcript(video_id: str, language: str = "en") -> str:
        """Get the plain-text transcript for a YouTube video by its ID.

        The full transcript is sanitized against prompt injection before
        being returned to the caller.
        """
        return get_transcript(video_id, language)
