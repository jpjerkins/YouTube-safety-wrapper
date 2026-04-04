---
name: youtube
description: Fetch YouTube video transcripts and metadata via the safety wrapper. Use when Phil shares a YouTube URL and wants a summary, transcript, or to capture a video as a note.
---

# YouTube Safety Wrapper

Fetches transcripts and metadata from YouTube videos. Content is sanitized against prompt injection before reaching you.

**Base URL:** `http://thejerkins.duckdns.org:8004`

## When to Use

- Phil shares a YouTube URL and wants it summarized
- Phil wants a transcript from a video
- Phil wants to capture a video as an Obsidian note
- Referenced by the `open-brain` skill's capture workflow

## Endpoints

### Get transcript

```bash
curl -s "http://thejerkins.duckdns.org:8004/transcript?url=YOUTUBE_URL"
```

Returns: sanitized plain text transcript.

### Get video metadata

```bash
curl -s "http://thejerkins.duckdns.org:8004/video-metadata?url=YOUTUBE_URL" | python3 -m json.tool
```

Returns: JSON with `title`, `description`, `channel`, `upload_date`, `webpage_url`, and more.

## Notes

- URL formats supported: `youtube.com/watch?v=`, `youtu.be/`, YouTube Shorts
- Transcripts can be long — summarize rather than dumping raw text into context
- The safety wrapper strips potential prompt injection from titles, descriptions, and transcript text
