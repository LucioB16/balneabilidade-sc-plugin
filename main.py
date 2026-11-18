"""Guarded production entry point for the pinned Streamable HTTP MCP server."""

from __future__ import annotations

import os

import uvicorn
from balneabilidade_sc_mcp.http_server import app as upstream_app

from guard import PublicMcpGuard

app = PublicMcpGuard(upstream_app)


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
