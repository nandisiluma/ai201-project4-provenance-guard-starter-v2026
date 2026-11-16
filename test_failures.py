#!/usr/bin/env python3
"""
Failure-path tests for /submit (criterion 11).

    python -m unittest test_failures -v

The model is stubbed and the audit log goes to a temp file. Failures are induced
by making `detector.model_signal` raise, because the real detector doesn't fail
on demand.
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
SECRET = "/Users/someone/private/path secret-token-123"


class FailurePathTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self._patches = [
            mock.patch.object(config, "LOG_DIR", tmp),
            mock.patch.object(config, "AUDIT_LOG", tmp / "audit.jsonl"),
        ]
        for p in self._patches:
            p.start()
        app_module.limiter.reset()
        self.client = app_module.app.test_client()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self._tmp.cleanup()

    def _submit(self, creator="writer"):
        return self.client.post("/submit", json={"text": TEXT, "creator_id": creator})

    def _fail_with(self, exc):
        with mock.patch.object(detector, "model_signal", side_effect=exc):
            return self._submit()

    def test_unexpected_exception_is_a_500_with_no_verdict(self):
        resp = self._fail_with(RuntimeError(SECRET))
        self.assertEqual(resp.status_code, 500)
        body = resp.get_json()
        self.assertEqual(body["error"], "internal_error")
        self.assertIs(body["evaluated"], False)
        for forbidden in ("label", "guess", "confidence", "model_score", "style_score"):
            self.assertNotIn(forbidden, body)

    def test_error_detail_stays_in_the_log_not_the_response(self):
        resp = self._fail_with(RuntimeError(SECRET))
        self.assertNotIn("secret-token-123", resp.get_data(as_text=True))
        self.assertNotIn("Traceback", resp.get_data(as_text=True))
        entry = audit.read_entries()[-1]
        self.assertIn("secret-token-123", entry["error_message"])

    def test_detector_unavailable_is_a_503(self):
        resp = self._fail_with(detector.DetectorUnavailable("model files missing"))
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(resp.get_json()["error"], "detector_unavailable")

    def test_every_failure_leaves_an_error_record(self):
        self._fail_with(RuntimeError("boom"))
        self._fail_with(detector.DetectorUnavailable("gone"))
        errors = [e for e in audit.read_entries() if e.get("event") == "error"]
        self.assertEqual(len(errors), 2)
        for e in errors:
            for field in ("creator_id", "reason", "http_status", "error_type",
                          "error_message", "duration_ms", "input_chars", "timestamp"):
                self.assertIn(field, e)
        self.assertEqual({e["http_status"] for e in errors}, {500, 503})

    def test_a_failure_leaves_no_decision_to_appeal(self):
        self._fail_with(RuntimeError("boom"))
        decisions = [e for e in audit.read_entries() if e.get("event") not in ("error", "rejected")]
        self.assertEqual(decisions, [])

    def test_service_recovers_after_a_failure(self):
        self._fail_with(RuntimeError("boom"))
        with mock.patch.object(detector, "model_signal", lambda text: 0.5):
            self.assertEqual(self._submit("another").status_code, 200)
        self.assertEqual(self.client.post("/ping", json={"message": "hi"}).status_code, 200)

    def test_input_with_no_readable_words_is_refused_not_scored(self):
        with mock.patch.object(detector, "model_signal", side_effect=AssertionError("must not be scored")):
            resp = self.client.post("/submit", json={"text": "🙂🙂🙂 ???", "creator_id": "w"})
        self.assertEqual(resp.status_code, 422)
        self.assertNotIn("label", resp.get_json())
        self.assertEqual(audit.read_entries()[-1]["reason"], "no_readable_text")


if __name__ == "__main__":
    unittest.main(verbosity=2)
