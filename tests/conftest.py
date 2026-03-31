"""Pytest configuration and fixtures."""
import os
import tempfile
import sys
from unittest.mock import patch, MagicMock

# Create persistent temporary API key file before importing youtube_mcp modules
_temp_dir = tempfile.mkdtemp()
_temp_key_file = os.path.join(_temp_dir, "api_key.txt")
with open(_temp_key_file, 'w') as f:
    f.write("sk-fake-api-key-for-testing")

# Set the environment variable
os.environ["OPENROUTER_API_KEY_FILE"] = _temp_key_file

# Patch OpenAI so we don't make actual API calls
sys.modules["openai"] = MagicMock()
