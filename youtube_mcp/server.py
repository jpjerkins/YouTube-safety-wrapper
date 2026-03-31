"""YouTube MCP + REST server entry point.

Exposes YouTube tools via two interfaces on PORT (default 8004):
  - MCP over SSE at /mcp  (for AI agents)
  - REST API at /transcript  (for conventional HTTP clients)

All untrusted YouTube content is scrubbed by a sandboxed LLM before being
returned. Requires vault-t2 FUSE mount for the OpenRouter API key.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from mcp.server.fastmcp import FastMCP
from youtube_mcp.tools import register_tools
from youtube_mcp.transcript import get_transcript

_PORT = int(os.getenv("PORT", "8004"))

mcp = FastMCP("YouTube")
register_tools(mcp)

app = FastAPI()
app.mount("/mcp", mcp.sse_app())


@app.get("/transcript", response_class=PlainTextResponse)
def transcript(url: str, language: str = "en") -> str:
    """Return the sanitized plain-text transcript for a YouTube video URL."""
    try:
        return get_transcript(url, language)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=_PORT)
