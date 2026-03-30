FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd -g 50011 youtube-mcp && useradd -u 50011 -g 50011 -s /bin/false -M youtube-mcp
COPY youtube_mcp/ ./youtube_mcp/
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh
USER 50011
EXPOSE 8004
CMD ["/app/entrypoint.sh"]
