#!/usr/bin/env python3
"""Run the five positive MCP *tool-level* review checks against a live endpoint.

This is a one-shot, serial integration check. It cannot assess LLM tool
selection, response language, or the three cases where ChatGPT must not
invoke the plugin. Those require a real ChatGPT review and recording.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.check_remote_mcp import DEFAULT_URL, EXPECTED_TOOLS, invoke


class McpClient:
    def __init__(self, url: str, timeout: float) -> None:
        self.url = url
        self.timeout = timeout
        self.protocol: str | None = None
        self._request_id = 0

    def rpc(self, method: str, params: dict) -> dict:
        self._request_id += 1
        result, _elapsed = invoke(
            self.url, method, self._request_id, params, self.timeout, self.protocol
        )
        return result

    def initialize(self) -> None:
        initialized = self.rpc(
            "initialize",
            {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "balneabilidade-review-check", "version": "1.0"},
            },
        )
        if initialized.get("serverInfo", {}).get("name") != "balneabilidade-sc-mcp":
            raise ValueError("Unexpected MCP server")
        self.protocol = initialized.get("protocolVersion")
        if not self.protocol:
            raise ValueError("Missing negotiated protocol")
        listing = self.rpc("tools/list", {})
        actual = {tool.get("name") for tool in listing.get("tools", [])}
        if actual != EXPECTED_TOOLS:
            raise ValueError(f"Unexpected MCP tools: {sorted(actual)}")

    def call(self, name: str, arguments: dict) -> dict:
        result = self.rpc("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError"):
            raise ValueError(f"{name} reported a tool error")
        data = result.get("structuredContent")
        if not isinstance(data, dict):
            raise ValueError(f"{name} returned no structuredContent")
        if data.get("warnings"):
            print(f"WARNING {name}: {len(data['warnings'])} source warnings")
        return data


def canonical_search(client: McpClient, query: str, municipality: str, name: str) -> None:
    result = client.call("search_beaches", {"query": query, "municipality": municipality})
    if not any(
        row.get("beach_name") == name and row.get("municipality") == municipality
        for row in result.get("matches", [])
    ):
        raise ValueError(f"Could not resolve {name} in {municipality}")


def latest_status(client: McpClient, beach: str, municipality: str) -> dict:
    data = client.call(
        "get_bathing_status", {"beach": beach, "municipality": municipality}
    )
    if data.get("provider") != "IMA/SC":
        raise ValueError(f"Unexpected data provider for {beach}")
    resolved = data.get("beach", {})
    if resolved.get("municipality") != municipality:
        raise ValueError(f"Wrong municipality for {beach}")
    if not isinstance(data.get("points"), list) or not data["points"]:
        raise ValueError(f"No sampling-point results for {beach}")
    if not data.get("bulletin", {}).get("bulletin_date"):
        raise ValueError(f"No published bulletin date for {beach}")
    for point in data["points"]:
        if not point.get("classification") or not point.get("sample_date"):
            raise ValueError(f"Missing point-level classification or date for {beach}")
    counts = Counter(p["classification"] for p in data["points"])
    return {
        "beach": resolved.get("beach_name"),
        "municipality": municipality,
        "bulletin_date": data["bulletin"]["bulletin_date"],
        "summary_status": data.get("summary", {}).get("status"),
        "points": len(data["points"]),
        "classifications": dict(sorted(counts.items())),
        "improper_points": [
            {"name": p.get("point_name"), "sample_date": p.get("sample_date")}
            for p in data["points"] if p["classification"] == "improper"
        ],
    }


def complete_2025_history(client: McpClient, *, max_pages: int) -> dict:
    query = {
        "beach": "Praia do Campeche",
        "municipality": "Florianópolis",
        "from_date": "2025-01-01",
        "to_date": "2025-12-31",
        "limit": 50,
    }
    records: list[dict] = []
    pages = 0
    cursor: str | None = None
    coverage: dict = {}
    seen_cursors: set[str] = set()
    while True:
        if pages >= max_pages:
            raise ValueError("History pagination exceeded max_pages before completion")
        arguments = dict(query)
        if cursor:
            arguments["cursor"] = cursor
        data = client.call("get_bathing_history", arguments)
        pages += 1
        coverage = data.get("coverage") or {}
        chunk = data.get("records", [])
        if not isinstance(chunk, list):
            raise ValueError("History records must be a list")
        records.extend(chunk)
        cursor = data.get("next_cursor")
        if not cursor:
            break
        if cursor in seen_cursors:
            raise ValueError("Repeated pagination cursor")
        seen_cursors.add(cursor)
    if not records or 2025 not in coverage.get("years_with_data", []):
        raise ValueError("Missing documented history for 2025")
    for record in records:
        date = record.get("sample_date", "")
        if not ("2025-01-01" <= date <= "2025-12-31"):
            raise ValueError(f"History contains out-of-range measurement: {date}")
        if not record.get("point_name") or not record.get("classification"):
            raise ValueError("History contains an unlabelled measurement")
    statuses = Counter(row["classification"] for row in records)
    return {
        "beach": "Praia do Campeche",
        "municipality": "Florianópolis",
        "period": ["2025-01-01", "2025-12-31"],
        "records": len(records),
        "pages": pages,
        "sampling_points": sorted({row["point_name"] for row in records}),
        "first_sample_date": min(row["sample_date"] for row in records),
        "last_sample_date": max(row["sample_date"] for row in records),
        "classifications": dict(sorted(statuses.items())),
        "coverage": coverage,
    }


def run(url: str, timeout: float, max_pages: int) -> dict[str, Any]:
    client = McpClient(url, timeout)
    client.initialize()
    print("PASS MCP initialize and tools/list (5 tools)", flush=True)

    positives: list[dict] = []

    # P1: Search the loose user alias by its distinctive name, then resolve
    # to IMA/SC's precise canonical name for the status call.
    canonical_search(client, "Perequê", "Porto Belo", "Praia de Perequê")
    positives.append({
        "id": "P1", "status": "tool_passed",
        "result": latest_status(client, "Praia de Perequê", "Porto Belo"),
    })
    print("PASS P1 Perequê search + status", flush=True)

    positives.append({
        "id": "P2", "status": "tool_passed",
        "result": latest_status(client, "Praia Brava", "Florianópolis"),
    })
    print("PASS P2 Praia Brava point-level status", flush=True)

    canonical_search(client, "Campeche", "Florianópolis", "Praia do Campeche")
    positives.append({
        "id": "P3", "status": "tool_passed",
        "result": complete_2025_history(client, max_pages=max_pages),
    })
    print("PASS P3 Campeche complete 2025 history", flush=True)

    positives.append({
        "id": "P4", "status": "tool_passed",
        "result": latest_status(client, "Praia de Zimbros", "Bombinhas"),
    })
    print("PASS P4 Zimbros dated status", flush=True)

    canonical_search(client, "Praia de Garopaba", "Garopaba", "Praia de Garopaba")
    positives.append({
        "id": "P5", "status": "tool_passed",
        "result": latest_status(client, "Praia de Garopaba", "Garopaba"),
    })
    print("PASS P5 Garopaba search + status", flush=True)

    print("PENDING N1–N3: requires actual ChatGPT no-tool-selection review", flush=True)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": url,
        "method": "direct MCP tool calls, not a ChatGPT language-model run",
        "positive": positives,
        "negative": [
            {"id": "N1", "status": "requires_chatgpt_review"},
            {"id": "N2", "status": "requires_chatgpt_review"},
            {"id": "N3", "status": "requires_chatgpt_review"},
        ],
        "video_recorded": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--output", help="Optional path for a local JSON result report")
    args = parser.parse_args()
    if args.max_pages < 1 or args.timeout <= 0:
        parser.error("--max-pages and --timeout must be positive")
    try:
        report = run(args.url, args.timeout, args.max_pages)
        if args.output:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    except (ValueError, OSError, TimeoutError) as exc:
        print(f"FAIL review tool checks: {exc}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
