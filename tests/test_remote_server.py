from __future__ import annotations

import unittest

import httpx
from starlette.testclient import TestClient

from balneabilidade_sc_mcp.http import ImaHttpClient
from balneabilidade_sc_mcp.provider import ImaProvider
from balneabilidade_sc_mcp.server import create_streamable_http_app


class StreamableHttpTests(unittest.TestCase):
    def test_server_initializes_and_advertises_the_five_tools(self) -> None:
        http_client = ImaHttpClient(transport=httpx.MockTransport(lambda _: httpx.Response(200)))
        provider = ImaProvider(http=http_client, own_http=True)
        app = create_streamable_http_app(provider)
        headers = {"accept": "application/json, text/event-stream", "content-type": "application/json"}
        with TestClient(app, base_url="http://127.0.0.1") as client:
            initialized = client.post(
                "/mcp",
                headers=headers,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "clientInfo": {"name": "plugin-ci", "version": "1.0.0"},
                    },
                },
            )
            self.assertEqual(initialized.status_code, 200, initialized.text)
            self.assertEqual(initialized.json()["result"]["serverInfo"]["name"], "balneabilidade-sc-mcp")

            result = client.post(
                "/mcp",
                headers=headers,
                json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            )
            self.assertEqual(result.status_code, 200, result.text)
            tools = result.json()["result"]["tools"]
            self.assertEqual(
                {tool["name"] for tool in tools},
                {
                    "search_beaches",
                    "get_sampling_points",
                    "get_bathing_status",
                    "get_bathing_history",
                    "get_bulletin_page",
                },
            )
            self.assertTrue(all(tool["annotations"]["readOnlyHint"] is True for tool in tools))
            self.assertTrue(all(tool["annotations"]["openWorldHint"] is True for tool in tools))
            self.assertTrue(all(tool["annotations"]["destructiveHint"] is False for tool in tools))


if __name__ == "__main__":
    unittest.main()
