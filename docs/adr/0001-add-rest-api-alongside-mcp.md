# ADR 0001: Add REST API alongside MCP server

**Date:** 2026-03-30  
**Status:** Accepted

---

## Context

The YouTube safety wrapper exposes its tools (search, metadata, transcript) via MCP over SSE. MCP is well-suited for AI agent use, but conventional HTTP clients — such as the sibling `shortcuts-api` project — cannot consume it directly.

## Decision

Wrap the MCP server with FastAPI as the outer ASGI application. REST routes are added at the root level; the MCP SSE app mounts at `/mcp`. Both share the same port (8004), process, and domain functions.

Initial REST surface: `GET /transcript?url=<youtube_url>&language=en` → `text/plain`.

Domain functions (`get_transcript`, `get_video_metadata`) are updated to accept a full YouTube URL **or** a bare video ID, since yt-dlp resolves both natively. This change benefits both the REST and MCP layers.

## Consequences

- MCP clients must update their server URL to include the `/mcp` path prefix.
- FastAPI's automatic `/docs` endpoint is available at no extra cost.
- Future REST endpoints (metadata, search) can be added incrementally without architectural change.
- No authentication is added; the API is intended for internal network use only.
