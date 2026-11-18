from __future__ import annotations

import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

from guard import PublicMcpGuard

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_COMMIT = "fee46b0990fa4a86aa61c89d5564157b1d97782e"


class EnzonicEntrypointTests(unittest.TestCase):
    def test_main_py_starts_guarded_mcp_on_provider_port(self) -> None:
        with patch.dict("os.environ", {"PORT": "28982"}), patch("uvicorn.run") as start:
            runpy.run_path(str(ROOT / "main.py"), run_name="__main__")
        start.assert_called_once()
        args, kwargs = start.call_args
        from main import DomainChallengeApp

        self.assertIsInstance(args[0], DomainChallengeApp)
        self.assertIsInstance(args[0].downstream, PublicMcpGuard)
        self.assertEqual(kwargs["host"], "0.0.0.0")
        self.assertEqual(kwargs["port"], 28982)
        self.assertFalse(kwargs["access_log"])

    def test_requirements_use_the_verified_immutable_archive(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn(
            f"balneabilidade-sc-mcp[mcp] @ https://github.com/LucioB16/"
            f"balneabilidade-sc-mcp/archive/{UPSTREAM_COMMIT}.zip",
            requirements,
        )
        self.assertIn("uvicorn>=0.34,<1", requirements)
        self.assertNotIn("git+", requirements)


if __name__ == "__main__":
    unittest.main()
