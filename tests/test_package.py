from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import zipfile

from scripts.build_plugin_archive import PackageError, apply_submission_metadata, build_archive, validate_https_url


ROOT = Path(__file__).resolve().parents[1]


class PackageMetadataTests(unittest.TestCase):
    def test_listing_manifest_has_valid_lengths_and_review_case_counts(self) -> None:
        manifest = json.loads((ROOT / "plugin/plugin.json").read_text(encoding="utf-8"))
        interface = manifest["extensions"]["com.openai"]["interface"]
        cases = manifest["extensions"]["com.openai"]["review"]["test_cases"]
        self.assertLessEqual(len(interface["displayName"]), 30)
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertNotIn("official", interface["shortDescription"].lower())
        self.assertIn("independent", interface["longDescription"].lower())
        translations = manifest["extensions"]["com.openai"]["publication"]["translations"]
        for locale in ("es-AR", "pt-BR"):
            self.assertLessEqual(len(translations[locale]["subtitle"]), 30)
            self.assertNotIn("oficial", translations[locale]["subtitle"].lower())
        self.assertLessEqual(len(interface["longDescription"]), 4000)
        self.assertEqual(len(cases["positive"]), 5)
        self.assertEqual(len(cases["negative"]), 3)
        for case in cases["positive"]:
            self.assertTrue(case["description"].strip())
            self.assertTrue(case["prompt"].strip())
            self.assertIsInstance(case["tools_triggered"], str)
            self.assertIsInstance(case["expected_behavior"], str)
        for case in cases["negative"]:
            self.assertTrue(case["description"].strip())
            self.assertTrue(case["prompt"].strip())
            self.assertIsInstance(case["expected_behavior"], str)

    def test_icon_is_square_and_large_enough_for_public_listing(self) -> None:
        data = (ROOT / "plugin/assets/icon.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        self.assertGreaterEqual(width, 256)
        self.assertGreaterEqual(height, 256)
        self.assertEqual(width, height)

    def test_https_url_shape_and_placeholder_rejection(self) -> None:
        self.assertEqual(validate_https_url("https://github.com/LucioB16", "websiteURL"), "https://github.com/LucioB16")
        for url in ("http://example.org/policy", "https://localhost/", "https://policy.example.test/privacy"):
            with self.subTest(url=url), self.assertRaises(PackageError):
                validate_https_url(url, "privacyPolicyURL")


    def test_draft_metadata_is_grounded_and_omits_missing_optional_fields(self) -> None:
        metadata = json.loads((ROOT / "submission/metadata.template.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "plugin/plugin.json").read_text(encoding="utf-8"))
        apply_submission_metadata(manifest, metadata)
        ext = manifest["extensions"]["com.openai"]
        self.assertEqual(ext["interface"]["developerName"], "Lucio Bottacin")
        self.assertTrue(ext["interface"]["privacyPolicyURL"].startswith("https://"))
        self.assertTrue(ext["interface"]["termsOfServiceURL"].startswith("https://"))
        self.assertIs(ext["review"]["commerce"], False)
        self.assertNotIn("demo_recording_url", ext["review"])
        self.assertNotIn("countries", ext["publication"])

    def test_draft_zip_builds_and_final_mode_rejects_missing_video(self) -> None:
        metadata = ROOT / "submission/metadata.template.json"
        with TemporaryDirectory() as temp:
            zip_path = Path(temp) / "draft.zip"
            build_archive("https://balneabilidade-sc.enzonic.dev/mcp", metadata, zip_path)
            with zipfile.ZipFile(zip_path) as archive:
                names = archive.namelist()
                self.assertIn("balneabilidade-sc/plugin.json", names)
                self.assertIn("balneabilidade-sc/mcp.json", names)
                manifest = json.loads(archive.read("balneabilidade-sc/plugin.json"))
                self.assertNotIn("demo_recording_url", manifest["extensions"]["com.openai"]["review"])
            with self.assertRaisesRegex(PackageError, "Final review requires"):
                build_archive("https://balneabilidade-sc.enzonic.dev/mcp", metadata, zip_path, require_demo=True)

    def test_submission_builder_requires_unprovided_publisher_facts(self) -> None:
        manifest = json.loads((ROOT / "plugin/plugin.json").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(PackageError, "verified individual or business identity"):
            apply_submission_metadata(manifest, {})


if __name__ == "__main__":
    unittest.main()
