from __future__ import annotations

import asyncio
import unittest

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from guard import PublicMcpGuard


async def echo(request):
    return PlainTextResponse((await request.body()).decode("utf-8"))


async def get(request):
    return PlainTextResponse("stream request accepted")


class GuardTests(unittest.TestCase):
    def test_regular_post_and_get_pass_through(self):
        app = PublicMcpGuard(Starlette(routes=[
            Route("/mcp", echo, methods=["POST"]),
            Route("/mcp", get, methods=["GET"]),
        ]))
        with TestClient(app) as client:
            self.assertEqual(client.post("/mcp", content=b"hello").text, "hello")
            self.assertEqual(client.get("/mcp").text, "stream request accepted")

    def test_sliding_window_returns_429_then_recovers(self):
        now = [10.0]
        app = PublicMcpGuard(
            Starlette(routes=[Route("/mcp", echo, methods=["POST"])]),
            requests_per_minute=2,
            clock=lambda: now[0],
        )
        with TestClient(app) as client:
            self.assertEqual(client.post("/mcp", content=b"a").status_code, 200)
            self.assertEqual(client.post("/mcp", content=b"b").status_code, 200)
            limited = client.post("/mcp", content=b"c")
            self.assertEqual(limited.status_code, 429)
            self.assertEqual(limited.headers["retry-after"], "5")
            now[0] += 61
            self.assertEqual(client.post("/mcp", content=b"d").status_code, 200)

    def test_declared_and_chunked_oversized_bodies_are_rejected(self):
        app = PublicMcpGuard(
            Starlette(routes=[Route("/mcp", echo, methods=["POST"])]),
            max_body_bytes=4,
        )
        with TestClient(app) as client:
            self.assertEqual(client.post("/mcp", content=b"abcde").status_code, 413)
            self.assertEqual(client.post("/mcp", content=b"abcd").status_code, 200)

        async def direct_test():
            chunks = [
                {"type": "http.request", "body": b"abc", "more_body": True},
                {"type": "http.request", "body": b"de", "more_body": False},
            ]
            sent = []

            async def receive():
                return chunks.pop(0)

            async def send(message):
                sent.append(message)

            await app({"type": "http", "path": "/mcp", "method": "POST", "headers": []}, receive, send)
            self.assertEqual(sent[0]["status"], 413)

        asyncio.run(direct_test())

    def test_concurrent_post_rejected_without_stalling_other_request(self):
        async def run():
            hold = asyncio.Event()
            started = asyncio.Event()

            async def downstream(scope, receive, send):
                started.set()
                await hold.wait()
                await send({"type": "http.response.start", "status": 200, "headers": []})
                await send({"type": "http.response.body", "body": b"ok"})

            app = PublicMcpGuard(downstream, concurrent_posts=1)

            async def invoke():
                sent = []

                async def receive():
                    return {"type": "http.request", "body": b"{}", "more_body": False}

                async def send(message):
                    sent.append(message)

                await app({"type": "http", "path": "/mcp", "method": "POST", "headers": []}, receive, send)
                return sent

            pending = asyncio.create_task(invoke())
            await started.wait()
            second = await invoke()
            self.assertEqual(second[0]["status"], 503)
            hold.set()
            first = await pending
            self.assertEqual(first[0]["status"], 200)

        asyncio.run(run())

    def test_lifespan_not_intercepted(self):
        seen = []

        async def downstream(scope, receive, send):
            seen.append(scope["type"])

        app = PublicMcpGuard(downstream)
        asyncio.run(app({"type": "lifespan"}, None, None))
        self.assertEqual(seen, ["lifespan"])
