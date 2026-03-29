FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY youtube_mcp/ ./youtube_mcp/
EXPOSE 8004
CMD ["python", "-c", "from youtube_mcp.server import mcp; mcp.run(transport='sse')"]
