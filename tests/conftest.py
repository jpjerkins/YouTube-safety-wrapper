"""Pytest configuration and fixtures.

Module-level setup runs before any imports of youtube_mcp modules.
sanitizer.py reads the vault key file at import time, so we must provide
a fake key file and mock out openai before the first test collection.
"""
import atexit
import os
import shutil
import sys
import tempfile
from unittest.mock import MagicMock

_temp_dir = tempfile.mkdtemp()
_temp_key_file = os.path.join(_temp_dir, "api_key.txt")
with open(_temp_key_file, "w") as f:
    f.write("sk-fake-api-key-for-testing")

os.environ["OPENROUTER_API_KEY_FILE"] = _temp_key_file
sys.modules["openai"] = MagicMock()

atexit.register(shutil.rmtree, _temp_dir, ignore_errors=True)
