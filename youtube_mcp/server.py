"""YouTube MCP server entry point.

Exposes YouTube search, metadata, and transcript extraction as MCP tools
via yt-dlp. All untrusted YouTube content is scrubbed by a sandboxed LLM
(dual-LLM pattern) before being returned to the caller.

Transport: SSE (HTTP) on PORT (default 8004).
Requires: ANTHROPIC_API_KEY env var.
"""
import os
from mcp.server.fastmcp import FastMCP
from youtube_mcp.tools import register_tools

_PORT = int(os.getenv("PORT", "8004"))

mcp = FastMCP("YouTube", host="0.0.0.0", port=_PORT)
register_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse")
