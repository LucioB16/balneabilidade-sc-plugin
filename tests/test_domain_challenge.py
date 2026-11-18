from __future__ import annotations

import asyncio
import unittest
from unittest.mock import patch

from main import DomainChallengeApp


async def send_challenge(method: str) -> list[dict]:
    """Exercise the challenge route directly, without starting MCP lifespan."""
    events: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        events.append(message)

    app = DomainChallengeApp(downstream=None)
    scope = {"type": "http", "method": method,
             "path": "/.well-known/openai-apps-challenge"}
    await app(scope, receive, send)
    return events


class DomainChallengeTests(unittest.TestCase):
    def test_unconfigured_challenge_is_404(self) -> None:
        with patch.dict("os.environ", {"OPENAI_APPS_CHALLENGE_TOKEN": ""}):
            result = asyncio.run(send_challenge("GET"))
        self.assertEqual(result[0]["status"], 404)
        self.assertEqual(result[1]["body"], b"")

    def test_challenge_returns_only_exact_token(self) -> None:
        token = "challenge_ABC_123.exact"
        with patch.dict("os.environ", {"OPENAI_APPS_CHALLENGE_TOKEN": token}):
            get_result = asyncio.run(send_challenge("GET"))
            head_result = asyncio.run(send_challenge("HEAD"))
            post_result = asyncio.run(send_challenge("POST"))
        self.assertEqual(get_result[0]["status"], 200)
        self.assertEqual(get_result[1]["body"], token.encode("utf-8"))
        headers = dict(get_result[0]["headers"])
        self.assertEqual(headers[b"content-type"], b"text/plain; charset=utf-8")
        self.assertEqual(headers[b"cache-control"], b"no-store")
        self.assertEqual(head_result[0]["status"], 200)
        self.assertEqual(head_result[1]["body"], b"")
        self.assertEqual(post_result[0]["status"], 405)

    def test_invalid_multiline_token_is_not_served(self) -> None:
        with patch.dict("os.environ", {"OPENAI_APPS_CHALLENGE_TOKEN": "a" + chr(10) + "b"}):
            result = asyncio.run(send_challenge("GET"))
        self.assertEqual(result[0]["status"], 404)


if __name__ == "__main__":
    unittest.main()
