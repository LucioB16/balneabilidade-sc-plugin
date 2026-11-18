from __future__ import annotations

import unittest

from scripts.check_legal_site import check


class LegalSiteTests(unittest.TestCase):
    def test_approved_pages_are_structurally_valid(self) -> None:
        self.assertEqual(check(require_publishable=False), [])

    def test_operator_contact_in_all_six_legal_pages(self) -> None:
        from scripts.check_legal_site import SITE, LEGAL_PAGES

        for name in LEGAL_PAGES:
            with self.subTest(name=name):
                content = (SITE / name).read_text(encoding="utf-8")
                self.assertIn("Lucio Bottacin", content)
                self.assertIn('href="mailto:luciobotacin@gmail.com"', content)

    def test_approved_pages_are_publishable(self) -> None:
        self.assertEqual(check(require_publishable=True), [])

    def test_pages_have_no_draft_language(self) -> None:
        from scripts.check_legal_site import SITE, LEGAL_PAGES
        for name in LEGAL_PAGES:
            with self.subTest(name=name):
                content = (SITE / name).read_text(encoding="utf-8")
                self.assertNotIn('content="noindex,nofollow"', content)
                self.assertNotIn('class="draft"', content)
                self.assertNotIn("This draft", content)
                self.assertNotIn("Este borrador", content)
                self.assertNotIn("Esta minuta", content)


if __name__ == "__main__":
    unittest.main()
