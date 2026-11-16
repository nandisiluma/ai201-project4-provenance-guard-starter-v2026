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

    def test_single_creator_id_is_limited(self):
        """Control: the existing per-creator limit still works."""
        statuses = self._statuses(lambda i: "one_writer")
        self.assertEqual(statuses.count(200), config.RATE_LIMIT_PER_MINUTE)
        self.assertIn(429, statuses)

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
