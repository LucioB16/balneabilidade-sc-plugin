from __future__ import annotations

import unittest

from starlette.testclient import TestClient

from main import app

HEADERS = {"accept": "application/json, text/event-stream", "content-type": "application/json"}


class GuardedMcpIntegrationTests(unittest.TestCase):
    def test_initialize_and_five_tools_through_actual_guard(self):
        # The upstream provider is not queried: this verifies the ASGI
        # lifespan, body replay, MCP transport, and JSON response together.
        with TestClient(app, base_url="http://127.0.0.1") as client:
            initialized = client.post(
                "/mcp",
                headers=HEADERS,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "clientInfo": {"name": "guarded-ci", "version": "1.0"},
                    },
                },
            )
            self.assertEqual(initialized.status_code, 200, initialized.text)
            self.assertEqual(initialized.json()["result"]["serverInfo"]["name"], "balneabilidade-sc-mcp")
            listed = client.post(
                "/mcp",
                headers=HEADERS,
                json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            )
            self.assertEqual(listed.status_code, 200, listed.text)
            names = {tool["name"] for tool in listed.json()["result"]["tools"]}
            self.assertEqual(
                names,
                {
                    "search_beaches",
                    "get_sampling_points",
                    "get_bathing_status",
                    "get_bathing_history",
                    "get_bulletin_page",
                },
            )
