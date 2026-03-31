# REST API Addition — Design Spec

**Date:** 2026-03-30  
**Project:** YouTube-safety-wrapper  

---

## Goal

Add a conventional HTTP REST API to the existing MCP server so sibling projects (e.g. `shortcuts-api`) can call YouTube functions directly without going through the MCP protocol.

Initial scope: transcript endpoint only.

---

## Architecture

FastAPI becomes the outer application on port 8004.  
The existing MCP SSE server mounts as a sub-app at `/mcp`.  
REST routes live at the root level alongside it.

```
port 8004
├── GET /transcript          ← new REST endpoint
└── /mcp                     ← existing MCP SSE server (mount point changes)
```

Both share the same process, port, and domain functions.

---

## Components

### `youtube_mcp/transcript.py`
- Change `get_transcript(video_id, language)` to accept a full YouTube URL **or** a bare video ID.
- yt-dlp resolves both natively; the function just stops assuming the input is an ID.

### `youtube_mcp/metadata.py`
- Same change as `transcript.py` — accept URL or ID for consistency.
- `search.py` is unchanged (its input is a query string, not a URL).

### `youtube_mcp/server.py`
- Create a `FastAPI` app instance.
- Add `GET /transcript?url=<youtube_url>` route — calls `get_transcript(url)` directly.
- Mount the MCP SSE app at `/mcp`.

---

## REST Endpoint

```
GET /transcript?url=<youtube_url>&language=en
```

| Parameter  | Required | Default | Notes                        |
|------------|----------|---------|------------------------------|
| `url`      | yes      | —       | Full YouTube URL or video ID |
| `language` | no       | `en`    | Transcript language code     |

**Response:** `200 text/plain` — sanitized transcript text.  
**Errors:** `404` if the video/transcript is not found, `500` for yt-dlp or sanitizer failures.

---

## MCP Clients

Existing MCP clients must update their server URL from:
- `http://host:8004/` → `http://host:8004/mcp`

The MCP tools (`search`, `video_metadata`, `transcript`) are unchanged. The `transcript` and `video_metadata` tools will gain URL support as a side effect of the domain function change.

---

## Out of Scope

- Authentication on the REST API (internal network only, behind Cloudflare tunnel if exposed)
- REST endpoints for search or metadata (can be added later)
- OpenAPI/Swagger customisation (FastAPI provides `/docs` automatically)
