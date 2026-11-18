from __future__ import annotations

import unittest
from unittest.mock import patch

from starlette.testclient import TestClient

from main import app


class DomainChallengeTests(unittest.TestCase):
    def test_unconfigured_challenge_is_404(self) -> None:
        with patch.dict("os.environ", {"OPENAI_APPS_CHALLENGE_TOKEN": ""}):
            with TestClient(app, base_url="http://127.0.0.1") as client:
                result = client.get("/.well-known/openai-apps-challenge")
        self.assertEqual(result.status_code, 404)

    def test_challenge_returns_only_exact_token(self) -> None:
        token = "challenge_ABC_123.exact"
        with patch.dict("os.environ", {"OPENAI_APPS_CHALLENGE_TOKEN": token}):
            with TestClient(app, base_url="http://127.0.0.1") as client:
                response = client.get("/.well-known/openai-apps-challenge")
                head = client.head("/.well-known/openai-apps-challenge")
                post = client.post("/.well-known/openai-apps-challenge")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, token.encode("utf-8"))
        self.assertEqual(response.headers["content-type"], "text/plain; charset=utf-8")
        self.assertEqual(response.headers["cache-control"], "no-store")
        self.assertEqual(head.status_code, 200)
        self.assertEqual(head.content, b"")
        self.assertEqual(post.status_code, 405)

    def test_invalid_multiline_token_is_not_served(self) -> None:
        with patch.dict("os.environ", {"OPENAI_APPS_CHALLENGE_TOKEN": "a\\nb"}):
            with TestClient(app, base_url="http://127.0.0.1") as client:
                response = client.get("/.well-known/openai-apps-challenge")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
