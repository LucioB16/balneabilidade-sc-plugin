"""Process-local admission control for the public, unauthenticated MCP route.

This limits *aggregate* work on one Python process, without trusting
X-Forwarded-For or assuming client IPs survive Enzonic's reverse proxy.
"""

from __future__ import annotations

import asyncio
import time
from collections import deque
from collections.abc import Callable
from typing import Any


class PublicMcpGuard:
    """Limit requests/minute, active POSTs and SSE streams, and POST body size."""

    def __init__(
        self,
        app: Any,
        *,
        requests_per_minute: int = 40,
        concurrent_posts: int = 2,
        concurrent_streams: int = 8,
        max_body_bytes: int = 262_144,
        body_timeout_seconds: float = 15.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if min(requests_per_minute, concurrent_posts, concurrent_streams, max_body_bytes) <= 0:
            raise ValueError("MCP limits must be positive")
        if body_timeout_seconds <= 0:
            raise ValueError("MCP body timeout must be positive")
        self.app = app
        self.requests_per_minute = requests_per_minute
        self.concurrent_posts = concurrent_posts
        self.concurrent_streams = concurrent_streams
        self.max_body_bytes = max_body_bytes
        self.body_timeout_seconds = body_timeout_seconds
        self.clock = clock
        self._lock = asyncio.Lock()
        self._recent: deque[float] = deque()
        self._posts = 0
        self._streams = 0

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope["type"] != "http" or scope.get("path", "").rstrip("/") != "/mcp":
            await self.app(scope, receive, send)
            return
        method = scope.get("method", "").upper()
        if method not in ("POST", "GET"):
            await self.app(scope, receive, send)
            return

        if method == "POST":
            lengths = [value for name, value in scope.get("headers", ()) if name.lower() == b"content-length"]
            if lengths:
                try:
                    declared = int(lengths[-1])
                except ValueError:
                    await _reject(send, 400, b"Invalid Content-Length")
                    return
                if declared < 0:
                    await _reject(send, 400, b"Invalid Content-Length")
                    return
                if declared > self.max_body_bytes:
                    await _reject(send, 413, b"MCP request body too large")
                    return

        async with self._lock:
            now = self.clock()
            while self._recent and self._recent[0] <= now - 60:
                self._recent.popleft()
            if len(self._recent) >= self.requests_per_minute:
                rejection = (429, b"MCP request rate limit exceeded")
            elif method == "POST" and self._posts >= self.concurrent_posts:
                rejection = (503, b"MCP request concurrency limit exceeded")
            elif method == "GET" and self._streams >= self.concurrent_streams:
                rejection = (503, b"MCP stream limit exceeded")
            else:
                rejection = None
                self._recent.append(now)
                if method == "POST":
                    self._posts += 1
                else:
                    self._streams += 1
        if rejection is not None:
            await _reject(send, *rejection, retry_after=b"5")
            return

        try:
            if method == "POST":
                chunks: list[bytes] = []
                total = 0
                try:
                    async with asyncio.timeout(self.body_timeout_seconds):
                        while True:
                            message = await receive()
                            if message["type"] == "http.disconnect":
                                return
                            if message["type"] != "http.request":
                                continue
                            part = message.get("body", b"")
                            total += len(part)
                            if total > self.max_body_bytes:
                                await _reject(send, 413, b"MCP request body too large")
                                return
                            chunks.append(part)
                            if not message.get("more_body", False):
                                break
                except TimeoutError:
                    await _reject(send, 408, b"MCP request body timeout")
                    return

                full_body = b"".join(chunks)
                provided = False

                async def replay_receive() -> dict:
                    nonlocal provided
                    if not provided:
                        provided = True
                        return {"type": "http.request", "body": full_body, "more_body": False}
                    return await receive()

                await self.app(scope, replay_receive, send)
            else:
                await self.app(scope, receive, send)
        finally:
            async with self._lock:
                if method == "POST":
                    self._posts -= 1
                else:
                    self._streams -= 1


async def _reject(send: Any, status: int, message: bytes, retry_after: bytes | None = None) -> None:
    headers = [
        (b"content-type", b"text/plain; charset=utf-8"),
        (b"content-length", str(len(message)).encode()),
    ]
    if retry_after is not None:
        headers.append((b"retry-after", retry_after))
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": message, "more_body": False})
