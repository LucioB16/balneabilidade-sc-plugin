"""Guarded production entry point for the pinned Streamable HTTP MCP server."""

from __future__ import annotations

import os

import uvicorn
from balneabilidade_sc_mcp.http_server import app as upstream_app

from guard import PublicMcpGuard

class DomainChallengeApp:
    """Serve OpenAI's exact domain verification token when configured.

    The token is set in Enzonic after the developer portal issues it.
    The challenge route is otherwise disabled (404), and /mcp is unchanged.
    """

    def __init__(self, downstream):
        self.downstream = downstream

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http" or scope.get("path") != "/.well-known/openai-apps-challenge":
            await self.downstream(scope, receive, send)
            return

        method = scope.get("method", "").upper()
        if method not in ("GET", "HEAD"):
            await send({"type": "http.response.start", "status": 405,
                        "headers": [(b"allow", b"GET, HEAD"), (b"content-length", b"0")]})
            await send({"type": "http.response.body", "body": b""})
            return

        token = os.environ.get("OPENAI_APPS_CHALLENGE_TOKEN", "")
        if not token or any(ch in token for ch in "\r\n") or len(token) > 4096:
            await send({"type": "http.response.start", "status": 404,
                        "headers": [(b"content-length", b"0"), (b"cache-control", b"no-store")]})
            await send({"type": "http.response.body", "body": b""})
            return

        body = token.encode("utf-8")
        headers = [
            (b"content-type", b"text/plain; charset=utf-8"),
            (b"content-length", str(len(body)).encode("ascii")),
            (b"cache-control", b"no-store"),
        ]
        await send({"type": "http.response.start", "status": 200, "headers": headers})
        await send({"type": "http.response.body", "body": b"" if method == "HEAD" else body})


app = DomainChallengeApp(PublicMcpGuard(upstream_app))


def main() -> None:
    uvicorn.run(
        app,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8000")),
        log_level="info",
        access_log=False,
    )


if __name__ == "__main__":
    main()
