import os
import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asr_comparison.adapters.vendorAdapter import canRunRealProvider
from asr_comparison.runner.inputGuard import validateInputGuard


class GuardTests(unittest.TestCase):
    def test_rejects_learner_data_before_any_adapter_call(self):
        result = validateInputGuard({
            "provider": "mock",
            "runId": "run-1",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture.wav",
            "sourceAudioHash": "hash-1",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "learnerId": "A-001",
            "textPassport": {
                "textId": "text-1",
                "textVersion": "v1",
                "regionalVariantSetId": "standard",
                "rightsStatus": "approved",
                "visibilityScope": "private_test",
                "workflowStatus": "approved",
            },
        })
        self.assertFalse(result["ok"])

    def test_rejects_unapproved_text(self):
        result = validateInputGuard({
            "provider": "mock",
            "runId": "run-2",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture.wav",
            "sourceAudioHash": "hash-2",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "textPassport": {
                "textId": "text-2",
                "textVersion": "v1",
                "regionalVariantSetId": "standard",
                "rightsStatus": "draft",
                "visibilityScope": "private_test",
                "workflowStatus": "approved",
            },
        })
        self.assertFalse(result["ok"])

    def test_accepts_safe_mock_input(self):
        result = validateInputGuard({
            "provider": "mock",
            "runId": "run-3",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture.wav",
            "sourceAudioHash": "hash-3",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "textPassport": {
                "textId": "text-3",
                "textVersion": "v1",
                "regionalVariantSetId": "standard",
                "rightsStatus": "approved",
                "visibilityScope": "private_test",
                "workflowStatus": "approved",
            },
        })
        self.assertTrue(result["ok"])

    def test_allows_local_authorized_real_provider_runs(self):
        original = {
            "ENABLE_REAL_VENDOR_RUNS": os.environ.get("ENABLE_REAL_VENDOR_RUNS"),
            "ASR_LOCAL_TEST_USERNAME": os.environ.get("ASR_LOCAL_TEST_USERNAME"),
            "ASR_LOCAL_TEST_PASSWORD": os.environ.get("ASR_LOCAL_TEST_PASSWORD"),
            "ASR_VENDOR_ALLOWLIST_TOKEN": os.environ.get("ASR_VENDOR_ALLOWLIST_TOKEN"),
        }
        try:
            os.environ["ENABLE_REAL_VENDOR_RUNS"] = "true"
            os.environ["ASR_LOCAL_TEST_USERNAME"] = "user1"
            os.environ["ASR_LOCAL_TEST_PASSWORD"] = "password1"
            os.environ["ASR_VENDOR_ALLOWLIST_TOKEN"] = "approved"

            self.assertTrue(canRunRealProvider("speechace"))
            self.assertTrue(canRunRealProvider("soapbox"))
        finally:
            for key, value in original.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
