from __future__ import annotations

from typing import Any, Literal

POLICY_VERSION = "RL-0.2-local-synthetic"

PolicyAction = Literal["prompt", "model", "stay_silent", "teacher_review", "analysis_unavailable"]


def applyEvidencePolicy(candidate: dict[str, Any]) -> dict[str, Any]:
    target = str(candidate.get("targetToken", "")).lower()
    heard = str(candidate.get("heardToken", "")).lower()
    confidence = float(candidate.get("confidence", 0.0) or 0.0)
    classification = str(candidate.get("classification", "")).lower()
    evidence = str(candidate.get("evidence", "")).lower()

    reason = ""
    if candidate.get("classification") is None or candidate.get("targetToken") is None:
        return {
            **candidate,
            "policyAction": "analysis_unavailable",
            "policyReason": "Malformed evidence payload; analysis unavailable.",
            "policyVersion": POLICY_VERSION,
        }

    if confidence < 0.72:
        reason = "Low confidence: no child-facing correction is permitted."
        return {
            **candidate,
            "policyAction": "stay_silent",
            "policyReason": reason,
            "policyVersion": POLICY_VERSION,
        }

    if (
        "accent" in classification
        or "dialect" in classification
        or "variation" in classification
        or "ambiguous" in classification
        or "near-homophone" in classification.lower()
        or "regional" in classification
        or "pause" in evidence
        or "hesitation" in evidence
    ):
        return {
            **candidate,
            "policyAction": "stay_silent",
            "policyReason": "The evidence may reflect accent, dialect, or legitimate variation; the safe result is silence.",
            "policyVersion": POLICY_VERSION,
        }

    if (
        "substitution" in classification
        or "omission" in classification
        or "insertion" in classification
        or "possible substitution" in evidence
        or "omission" in evidence
        or "insertion" in evidence
    ):
        return {
            **candidate,
            "policyAction": "teacher_review",
            "policyReason": "Possible mismatch exists, but adult review is required before any correction or final judgement.",
            "policyVersion": POLICY_VERSION,
        }

    if "self_correction" in classification or "self-correction" in evidence:
        return {
            **candidate,
            "policyAction": "teacher_review",
            "policyReason": "Self-correction in flight is preserved; no automatic final error is allowed.",
            "policyVersion": POLICY_VERSION,
        }

    return {
        **candidate,
        "policyAction": "teacher_review",
        "policyReason": "The supplied provider evidence is not safe for automatic child-facing action.",
        "policyVersion": POLICY_VERSION,
    }
