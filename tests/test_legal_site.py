from __future__ import annotations

import unittest

from scripts.check_legal_site import check


class LegalSiteTests(unittest.TestCase):
    def test_draft_pages_are_structurally_valid(self) -> None:
        self.assertEqual(check(require_publishable=False), [])

    def test_unreviewed_draft_cannot_be_published(self) -> None:
        problems = check(require_publishable=True)
        self.assertGreaterEqual(len(problems), 6)
        self.assertTrue(all("still " in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
