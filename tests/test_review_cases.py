"""Offline checks for the exactly-five/exactly-three initial review inventory."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.review_cases import McpClient, complete_2025_history

ROOT = Path(__file__).resolve().parents[1]


def test_review_inventory_count_and_required_fields():
    manifest = json.loads((ROOT / "plugin/plugin.json").read_text(encoding="utf-8"))
    review = manifest["extensions"]["com.openai"]["review"]["test_cases"]
    assert len(review["positive"]) == 5
    assert len(review["negative"]) == 3
    for case in review["positive"]:
        assert all(case.get(k) for k in ("description", "prompt", "tools_triggered", "expected_behavior"))
    for case in review["negative"]:
        assert all(case.get(k) for k in ("description", "prompt", "expected_behavior"))


def test_canonical_name_expectations_match_ima_catalog():
    manifest = json.loads((ROOT / "plugin/plugin.json").read_text(encoding="utf-8"))
    positive = manifest["extensions"]["com.openai"]["review"]["test_cases"]["positive"]
    assert "query=Perequê" in positive[0]["expected_behavior"]
    assert "Praia de Perequê" in positive[0]["expected_behavior"]
    assert positive[2]["tools_triggered"] == "search_beaches, get_bathing_history"
    assert "Praia do Campeche" in positive[2]["expected_behavior"]
    assert "next_cursor" in positive[2]["expected_behavior"]


def test_history_pagination_uses_all_pages_without_network():
    class Fake(McpClient):
        def __init__(self):
            self.calls = []

        def call(self, name: str, arguments: dict) -> dict:
            self.calls.append((name, arguments))
            if len(self.calls) == 1:
                return {
                    "records": [{"sample_date": "2025-12-02", "point_name": "Ponto 35", "classification": "proper"}],
                    "next_cursor": "1",
                    "coverage": {"years_with_data": [2025]},
                }
            return {
                "records": [{"sample_date": "2025-01-02", "point_name": "Ponto 73", "classification": "improper"}],
                "next_cursor": None,
                "coverage": {"years_with_data": [2025]},
            }
    client = Fake()
    summary = complete_2025_history(client, max_pages=2)
    assert summary["records"] == 2
    assert summary["pages"] == 2
    assert client.calls[0][1].get("cursor") is None
    assert client.calls[1][1]["cursor"] == "1"


def test_negative_prompts_are_manual_no_tool_cases():
    manifest = json.loads((ROOT / "plugin/plugin.json").read_text(encoding="utf-8"))
    negative = manifest["extensions"]["com.openai"]["review"]["test_cases"]["negative"]
    assert all("do not call" in case["expected_behavior"].lower() for case in negative)
