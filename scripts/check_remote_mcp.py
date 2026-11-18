#!/usr/bin/env python3
"""One-shot HTTPS/Streamable HTTP MCP smoke check after a manual restart."""

from __future__ import annotations

import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

EXPECTED_TOOLS = {
    "search_beaches",
    "get_sampling_points",
    "get_bathing_status",
    "get_bathing_history",
    "get_bulletin_page",
}
DEFAULT_URL = "https://balneabilidade-sc.enzonic.dev/mcp"


def invoke(url: str, method: str, request_id: int, params: dict, timeout: float, protocol: str | None = None) -> tuple[dict, float]:
    payload = json.dumps(
        {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
        ensure_ascii=False,
    ).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8", "Accept": "application/json, text/event-stream"}
    if protocol:
        headers["MCP-Protocol-Version"] = protocol
    request = Request(url, data=payload, headers=headers, method="POST")
    started = time.monotonic()
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get_content_type()
        if content_type != "application/json":
            raise ValueError(f"Expected JSON MCP response, received {content_type}")
        response_data = json.load(response)
    elapsed = time.monotonic() - started
    if response_data.get("jsonrpc") != "2.0" or response_data.get("id") != request_id or "error" in response_data:
        raise ValueError(f"Unexpected JSON-RPC response for {method}: {str(response_data)[:300]}")
    result = response_data.get("result")
    if not isinstance(result, dict):
        raise ValueError(f"Missing MCP result for {method}")
    return result, elapsed


def smoke(url: str, timeout: float, check_source: bool = False) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.path.rstrip("/") != "/mcp":
        raise ValueError("Use the HTTPS public /mcp endpoint (not a local port or preview)")

    initialized, elapsed = invoke(
        url, "initialize", 1,
        {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "post-restart-smoke", "version": "1.0"}},
        timeout,
    )
    protocol = initialized.get("protocolVersion")
    if not protocol or initialized.get("serverInfo", {}).get("name") != "balneabilidade-sc-mcp":
        raise ValueError("Wrong MCP server or invalid initialization")
    print(f"PASS initialize: {elapsed:.2f}s, protocol {protocol}")

    listing, elapsed = invoke(url, "tools/list", 2, {}, timeout, protocol)
    names = {tool.get("name") for tool in listing.get("tools", [])}
    if names != EXPECTED_TOOLS:
        raise ValueError(f"Unexpected MCP tools: {sorted(names)}")
    print(f"PASS tools/list: {elapsed:.2f}s, 5 tools")

    if check_source:
        result, elapsed = invoke(
            url, "tools/call", 3,
            {"name": "get_bathing_status", "arguments": {"beach": "Praia de Perequê", "municipality": "Porto Belo"}},
            timeout, protocol,
        )
        if result.get("isError"):
            raise ValueError(f"MCP tool error: {str(result)[:250]}")
        source = result.get("structuredContent", {})
        if source.get("provider") != "IMA/SC" or source.get("beach", {}).get("municipality") != "Porto Belo" or not source.get("points"):
            raise ValueError("Unexpected IMA/SC provider result")
        print(f"PASS IMA/SC call: {elapsed:.2f}s, {len(source['points'])} points, bulletin {source.get('bulletin', {}).get('bulletin_date')}")
        if source.get("bulletin_unverified") or source.get("warnings"):
            print("WARNING: unverified bulletin or provider warnings; inspect the source data")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=45)
    parser.add_argument("--check-source", action="store_true", help="Make one real IMA/SC call")
    args = parser.parse_args()
    try:
        smoke(args.url, args.timeout, args.check_source)
    except (ValueError, HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL remote MCP smoke check: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
