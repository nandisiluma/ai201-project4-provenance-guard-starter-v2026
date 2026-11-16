#!/usr/bin/env python3
"""
Rate-limit tests for /submit (Unit 9, step 1).

    python -m unittest test_rate_limit -v

The model is stubbed (no gpt2 load, no download) and the audit log is redirected
to a temp file, so this touches neither the real model nor logs/audit.jsonl.

Test 1 is the bug: the limit is keyed on the caller-supplied `creator_id`, so a
script that rotates it never hits a limit. It FAILS on the current code
(40 requests -> 40 x 200). Test 2 is the control: one creator_id is limited.
"""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import app as app_module
import audit
import config
import detector

TEXT = "The committee reviewed the proposal and decided to postpone the vote until spring."
N_REQUESTS = 40


class RateLimitTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self._patches = [
            mock.patch.object(config, "LOG_DIR", tmp),
            mock.patch.object(config, "AUDIT_LOG", tmp / "audit.jsonl"),
            mock.patch.object(detector, "model_signal", lambda text: 0.5),
        ]
        for p in self._patches:
            p.start()
        # Fresh quota for every test (in-memory storage is shared per process).
        app_module.limiter.reset()
        self.client = app_module.app.test_client()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self._tmp.cleanup()

    def _statuses(self, creator_for):
        return [
            self.client.post(
                "/submit", json={"text": TEXT, "creator_id": creator_for(i)}
            ).status_code
            for i in range(N_REQUESTS)
        ]

    def test_rotating_creator_id_from_one_address_is_limited(self):
        """A stranger rotating creator_id from ONE address must hit a 429."""
        statuses = self._statuses(lambda i: f"stranger_{i}")
        print(f"\n  rotating creator_id x{N_REQUESTS}: "
              f"{statuses.count(200)} x 200, {statuses.count(429)} x 429")
        self.assertIn(429, statuses, "40 requests from one address were never limited")
        self.assertEqual(statuses.count(200), config.RATE_LIMIT_ADDRESS_PER_MINUTE)
        self.assertEqual(statuses.count(429), N_REQUESTS - config.RATE_LIMIT_ADDRESS_PER_MINUTE)

    def test_single_creator_id_is_limited(self):
        """Control: the existing per-creator limit still works."""
        statuses = self._statuses(lambda i: "one_writer")
        self.assertEqual(statuses.count(200), config.RATE_LIMIT_PER_MINUTE)
        self.assertEqual(statuses.count(429), N_REQUESTS - config.RATE_LIMIT_PER_MINUTE)

    def test_writers_sharing_an_address_are_not_punished(self):
        """Four real writers behind one address, each within their own limit."""
        per = config.RATE_LIMIT_PER_MINUTE
        statuses = [
            self.client.post(
                "/submit", json={"text": TEXT, "creator_id": f"writer_{w}"}
            ).status_code
            for w in range(4) for _ in range(per)
        ]
        self.assertEqual(set(statuses), {200})

    def test_429_tells_the_caller_how_to_recover(self):
        """A 429 carries Retry-After, a structured body, and says nothing was evaluated."""
        resp = None
        for _ in range(config.RATE_LIMIT_PER_MINUTE + 1):
            resp = self.client.post("/submit", json={"text": TEXT, "creator_id": "one_writer"})
        self.assertEqual(resp.status_code, 429)

        header = resp.headers.get("Retry-After")
        self.assertIsNotNone(header, "429 is missing the Retry-After header")
        self.assertTrue(1 <= int(header) <= 61, f"Retry-After {header} outside the per-minute window")

        body = resp.get_json()
        self.assertEqual(body["error"], "rate_limited")
        self.assertEqual(body["retry_after"], int(header))
        self.assertEqual(body["scope"], "creator")
        self.assertIs(body["evaluated"], False)
        self.assertNotIn("label", body)  # a rejection must not look like a verdict

    def test_address_limit_is_reported_as_address_scope(self):
        resp = None
        for i in range(config.RATE_LIMIT_ADDRESS_PER_MINUTE + 1):
            resp = self.client.post("/submit", json={"text": TEXT, "creator_id": f"s_{i}"})
        self.assertEqual(resp.status_code, 429)
        self.assertEqual(resp.get_json()["scope"], "address")

    def test_rejection_is_audited_with_retry_after(self):
        for _ in range(config.RATE_LIMIT_PER_MINUTE + 1):
            self.client.post("/submit", json={"text": TEXT, "creator_id": "one_writer"})
        rejections = [e for e in audit.read_entries() if e.get("reason") == "rate_limited"]
        self.assertTrue(rejections, "no rate_limited entry in the audit log")
        self.assertIn("retry_after", rejections[-1])

    def test_every_429_has_exactly_one_audit_record(self):
        """Criterion 10: rejections and records match 1:1, in both flows."""
        for creator_for in (lambda i: f"stranger_{i}", lambda i: "one_writer"):
            app_module.limiter.reset()
            config.AUDIT_LOG.write_text("", encoding="utf-8")
            statuses = self._statuses(creator_for)
            records = [e for e in audit.read_entries() if e.get("reason") == "rate_limited"]
            self.assertEqual(len(records), statuses.count(429))
            for rec in records:
                for field in ("creator_id", "scope", "retry_after", "duration_ms"):
                    self.assertIn(field, rec)
                self.assertIsNotNone(rec["retry_after"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
