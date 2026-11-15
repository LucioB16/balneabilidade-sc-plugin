from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from scripts.check_remote_mcp import invoke, smoke


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
        self.headers = self

    def get_content_type(self):
        return "application/json"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, *args):
        return json.dumps(self.payload).encode("utf-8")


class SmokeTests(unittest.TestCase):
    def test_endpoint_must_be_https_mcp(self):
        with self.assertRaises(ValueError):
            smoke("http://127.0.0.1:8000/mcp", 5)
        with self.assertRaises(ValueError):
            smoke("https://example.org/nope", 5)

    def test_jsonrpc_error_is_rejected(self):
        reply = {"jsonrpc": "2.0", "id": 1, "error": {"code": -1}}
        with patch("scripts.check_remote_mcp.urlopen", return_value=FakeResponse(reply)):
            with self.assertRaises(ValueError):
                invoke("https://example.org/mcp", "initialize", 1, {}, 5)
