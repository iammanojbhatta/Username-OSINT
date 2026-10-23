#!/usr/bin/env python3
"""Offline tests for MANOJ USERNAME OSINT. No network access required.

Run from the repository root:
    python3 -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import load_sites, valid_username, validate_sites, verify, metadata


class TestUsernameRules(unittest.TestCase):
    def test_valid(self):
        for u in ("manojbhatta", "a.b-c_d", "A1", "x" * 64):
            self.assertTrue(valid_username(u), u)

    def test_invalid(self):
        for u in ("", "has space", "bad/name", "x" * 65, None, "üser"):
            self.assertFalse(valid_username(u), repr(u))


class TestSiteDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sites = load_sites()

    def test_database_loads(self):
        self.assertGreater(len(self.sites), 1000)

    def test_database_structurally_valid(self):
        self.assertEqual(validate_sites(self.sites), [])

    def test_every_url_formats(self):
        for s in self.sites:
            s["url"].format(username="testuser")  # raises if a stray brace exists


def canned(status, body=b"", final_url="https://example.com/testuser"):
    return {"status": status, "final_url": final_url, "headers": {},
            "body": body, "error": "", "chain": [final_url]}


SITE = {"name": "Example", "domain": "example.com", "category": "social",
        "url": "https://example.com/{username}",
        "positive": ["followers"], "negative": ["page not found"]}


class TestVerify(unittest.TestCase):
    def test_404_is_not_found_high(self):
        r = verify(SITE, "testuser", canned(404), SITE["url"].format(username="testuser"))
        self.assertEqual((r["status"], r["confidence"]), ("NOT_FOUND", "HIGH"))

    def test_403_is_blocked(self):
        r = verify(SITE, "testuser", canned(403), SITE["url"].format(username="testuser"))
        self.assertEqual(r["status"], "BLOCKED")

    def test_transport_failure_is_timeout(self):
        x = canned(None); x["error"] = "boom"
        r = verify(SITE, "testuser", x, SITE["url"].format(username="testuser"))
        self.assertEqual(r["status"], "TIMEOUT")

    def test_profile_signals_found(self):
        body = b"<html><title>testuser on Example</title><body>testuser has 42 followers</body></html>"
        r = verify(SITE, "testuser", canned(200, body), SITE["url"].format(username="testuser"))
        self.assertEqual(r["status"], "FOUND")

    def test_bare_200_is_unknown_never_found(self):
        r = verify(SITE, "testuser", canned(200, b"<html>hello</html>"),
                   SITE["url"].format(username="testuser"))
        self.assertEqual(r["status"], "UNKNOWN")


class TestMetadata(unittest.TestCase):
    def test_title_extraction(self):
        m = metadata(b"<html><head><title>  Hello   World </title></head></html>")
        self.assertEqual(m["title"], "Hello World")


if __name__ == "__main__":
    unittest.main()
