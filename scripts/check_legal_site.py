#!/usr/bin/env python3
"""Validate the Balneabilidade SC static legal pages before Pages deployment."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LEGAL_PAGES = [
    "privacy/index.html",
    "privacy/en/index.html",
    "privacy/es/index.html",
    "terms/index.html",
    "terms/en/index.html",
    "terms/es/index.html",
]


def check(*, require_publishable: bool) -> list[str]:
    problems: list[str] = []
    for name in ["index.html", "style.css", ".nojekyll", *LEGAL_PAGES]:
        path = SITE / name
        if not path.is_file():
            problems.append(f"missing file: site/{name}")
            continue
        if path.suffix != ".html":
            continue
        content = path.read_text(encoding="utf-8")
        if "<!doctype html>" not in content.lower():
            problems.append(f"invalid HTML doctype: site/{name}")
        if "https://github.com/LucioB16/balneabilidade-sc-plugin" not in content:
            problems.append(f"missing project attribution: site/{name}")
        if "<script" in content.lower():
            problems.append(f"unexpected JavaScript: site/{name}")
        if require_publishable:
            if 'content="noindex,nofollow"' in content:
                problems.append(f"still hidden from indexing: site/{name}")
            if 'class="draft"' in content:
                problems.append(f"still has legal draft notice: site/{name}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Require final approved text; reject draft banners")
    args = parser.parse_args()
    problems = check(require_publishable=args.publish)
    if problems:
        for problem in problems:
            print(f"ERROR {problem}")
        return 1
    print("PASS legal site files and links; publishability checked" if args.publish else "PASS legal draft structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
