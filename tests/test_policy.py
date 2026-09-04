import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.reader_leader.policy import POLICY_VERSION, applyEvidencePolicy


class PolicyTests(unittest.TestCase):
    def test_confidence_below_threshold_stays_silent(self):
        decision = applyEvidencePolicy({
            "targetToken": "river",
            "heardToken": "river",
            "confidence": 0.7199,
            "evidence": "low confidence",
            "classification": "clean_read",
        })
        self.assertEqual(decision["policyAction"], "stay_silent")
        self.assertEqual(decision["policyVersion"], POLICY_VERSION)

    def test_accent_variation_stays_silent(self):
        decision = applyEvidencePolicy({
            "targetToken": "cat",
            "heardToken": "kat",
            "confidence": 0.81,
            "evidence": "regional variation",
            "classification": "accent variation",
        })
        self.assertEqual(decision["policyAction"], "stay_silent")

    def test_substitution_requires_teacher_review(self):
        decision = applyEvidencePolicy({
            "targetToken": "red",
            "heardToken": "bed",
            "confidence": 0.82,
            "evidence": "likely substitution",
            "classification": "possible substitution",
        })
        self.assertEqual(decision["policyAction"], "teacher_review")

    def test_self_correction_is_review_not_final_error(self):
        decision = applyEvidencePolicy({
            "targetToken": "rain",
            "heardToken": "reign",
            "confidence": 0.78,
            "evidence": "self-correction in flight",
            "classification": "self_correction_in_flight",
        })
        self.assertEqual(decision["policyAction"], "teacher_review")


if __name__ == "__main__":
    unittest.main()
