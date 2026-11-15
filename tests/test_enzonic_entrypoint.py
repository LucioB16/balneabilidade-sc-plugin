from __future__ import annotations

import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_COMMIT = "fee46b0990fa4a86aa61c89d5564157b1d97782e"


class EnzonicEntrypointTests(unittest.TestCase):
    def test_main_py_delegates_to_upstream_http_server(self) -> None:
        # Do not start a listener; validate that the panel's main.py entry
        # actually calls the same installed HTTP command used by Docker.
        with patch("balneabilidade_sc_mcp.http_server.main") as start:
            runpy.run_path(str(ROOT / "main.py"), run_name="__main__")
        start.assert_called_once_with()

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
