#!/usr/bin/env python3
"""Build a plugin ZIP with verified metadata; require video for final review."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SOURCE = ROOT / "plugin"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
REQUIRED_URLS = ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")


class PackageError(ValueError):
    """Raised when submission inputs are incomplete or invalid."""


def validate_https_url(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PackageError(f"Missing required HTTPS URL: {field}")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        raise PackageError(f"{field} must be an absolute HTTPS URL without credentials or a fragment")
    if parsed.hostname in {"example.com", "example.org", "example.net", "localhost"} or parsed.hostname.endswith(
        (".test", ".example", ".invalid")
    ):
        raise PackageError(f"{field} cannot point to a placeholder or local host")
    return value


def apply_submission_metadata(manifest: dict, metadata: dict) -> None:
    interface = manifest["extensions"]["com.openai"]["interface"]
    review = manifest["extensions"]["com.openai"]["review"]
    publication = manifest["extensions"]["com.openai"]["publication"]

    developer_name = metadata.get("developerName")
    if not isinstance(developer_name, str) or not developer_name.strip() or len(developer_name) > 80:
        raise PackageError("Set developerName to the exact verified individual or business identity")
    interface["developerName"] = developer_name.strip()

    for field in REQUIRED_URLS:
        url = metadata.get(field, interface.get(field))
        interface[field] = validate_https_url(url, field)

    # OpenAI permits package upload before the video is ready.
    # The review submission, not the initial package upload, requires a demonstration.
    demo_url = metadata.get("demo_recording_url")
    if demo_url is not None:
        review["demo_recording_url"] = validate_https_url(demo_url, "demo_recording_url")

    commerce = metadata.get("commerce")
    commerce_description = metadata.get("commerce_description")
    if not isinstance(commerce, bool):
        raise PackageError("Choose and set the truthful commerce declaration")
    if not isinstance(commerce_description, str) or not commerce_description.strip():
        raise PackageError("Describe the plugin's commerce behavior in commerce_description")
    review["commerce"] = commerce
    review["commerce_description"] = commerce_description.strip()

    # Country targeting is optional. Null means no decision has been made:
    # omit the field rather than silently choosing global availability.
    countries = metadata.get("countries")
    if countries is not None:
        if not isinstance(countries, list) or any(
            not isinstance(country, str) or not re.fullmatch(r"[A-Z]{2}", country) for country in countries
        ) or len(countries) != len(set(countries)):
            raise PackageError("countries must be unique uppercase 2-letter codes, or null to omit")
        publication["countries"] = countries


def build_archive(mcp_url: str, metadata_path: Path, output_path: Path, *, require_demo: bool = False) -> Path:
    validate_https_url(mcp_url, "MCP endpoint")
    if not metadata_path.is_file():
        raise PackageError(f"Submission metadata file not found: {metadata_path}")

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        manifest = json.loads((PLUGIN_SOURCE / "plugin.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise PackageError(f"Could not read package metadata: {exc}") from exc
    if not isinstance(metadata, dict) or not isinstance(manifest, dict):
        raise PackageError("Manifest and submission metadata must be JSON objects")
    apply_submission_metadata(manifest, metadata)
    if require_demo and not manifest["extensions"]["com.openai"]["review"].get("demo_recording_url"):
        raise PackageError("Final review requires an actual reviewer-accessible demo_recording_url")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="balneabilidade-plugin-") as temporary:
        package_root = Path(temporary) / "balneabilidade-sc"
        shutil.copytree(PLUGIN_SOURCE, package_root)
        (package_root / "plugin.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (package_root / "mcp.json").write_text(
            json.dumps(
                {
                    "$schema": MCP_SCHEMA,
                    "mcpServers": {
                        "balneabilidade-sc": {"type": "streamable-http", "url": mcp_url}
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(package_root.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(Path(temporary)))

    with zipfile.ZipFile(output_path) as archive:
        names = archive.namelist()
        if not names or any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise PackageError("Generated archive has an invalid path")
        top_level = {Path(name).parts[0] for name in names}
        if top_level != {"balneabilidade-sc"}:
            raise PackageError("Archive must contain exactly one plugin directory")
        if "balneabilidade-sc/.app.json" in names:
            raise PackageError("Public upload must not contain an app binding")
        packaged_manifest = json.loads(archive.read("balneabilidade-sc/plugin.json"))
        packaged_mcp = json.loads(archive.read("balneabilidade-sc/mcp.json"))
        if packaged_manifest["extensions"]["com.openai"].get("apps"):
            raise PackageError("Public upload must not declare a private app binding")
        if set(packaged_mcp["mcpServers"]) != {"balneabilidade-sc"}:
            raise PackageError("Generated MCP manifest does not contain the expected server")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mcp-url", required=True, help="Verified stable production HTTPS /mcp endpoint")
    parser.add_argument(
        "--metadata",
        type=Path,
        default=ROOT / "submission/metadata.json",
        help="Private JSON file containing verified listing and publication facts",
    )
    parser.add_argument("--output", type=Path, help="Output ZIP path")
    parser.add_argument(
        "--require-demo", action="store_true",
        help="For final review, fail if a reviewer-accessible demo URL is missing",
    )
    args = parser.parse_args()
    version = json.loads((PLUGIN_SOURCE / "plugin.json").read_text(encoding="utf-8"))["version"]
    output = args.output or ROOT / "dist" / f"balneabilidade-sc-plugin-{version}.zip"
    try:
        result = build_archive(args.mcp_url, args.metadata, output, require_demo=args.require_demo)
    except PackageError as exc:
        parser.error(str(exc))
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
