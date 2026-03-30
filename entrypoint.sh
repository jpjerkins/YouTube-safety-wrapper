#!/bin/sh
# Source vault-t2 secrets into the environment, then start the server.
# Runs as UID 50011 — must match the ACL entry in /etc/vault-t2/envfiles.yaml.
set -a
# shellcheck disable=SC1091
. /run/vault-t2-fs/envfiles/youtube-mcp
set +a
exec python -m youtube_mcp.server
