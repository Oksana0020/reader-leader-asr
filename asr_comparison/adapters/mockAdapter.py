from __future__ import annotations

from typing import Any


def buildMockResponse(caseFamily: str) -> dict[str, Any]:
    base = {
        "vendor": "mock",
        "providerStatus": "ok",
        "vendorRequestId": "mock-request-001",
        "modelVersion": "mock-local-v1",
        "vendorRegion": "synthetic-test",
        "retentionMode": "synthetic-only",
        "policyVersion": "RL-0.2-local-synthetic",
        "timing": {
            "requestStartedAt": "2026-01-01T00:00:00.000Z",
            "responseReceivedAt": "2026-01-01T00:00:00.050Z",
            "endToEndMs": 50,
        },
    }

    if caseFamily == "exact_known_text":
        return {
            **base,
            "tokens": [{"referenceToken": "the", "heardToken": "the", "startMs": 120, "endMs": 220, "vendorConfidence": 0.93, "rawScore": 0.93, "eventClass": "exact"}],
        }
    if caseFamily == "substitution":
        return {
            **base,
            "tokens": [{"referenceToken": "red", "heardToken": "bed", "startMs": 300, "endMs": 420, "vendorConfidence": 0.78, "rawScore": 0.78, "eventClass": "substitution"}],
        }
    if caseFamily == "accent_dialect_variation":
        return {
            **base,
            "tokens": [{"referenceToken": "cat", "heardToken": "kat", "startMs": 1200, "endMs": 1350, "vendorConfidence": 0.81, "rawScore": 0.81, "eventClass": "variation"}],
        }
    if caseFamily == "ambiguous_near_homophone":
        return {
            **base,
            "tokens": [{"referenceToken": "their", "heardToken": "there", "startMs": 1400, "endMs": 1540, "vendorConfidence": 0.70, "rawScore": 0.70, "eventClass": "ambiguous"}],
        }
    if caseFamily == "hesitation_pause":
        return {
            **base,
            "tokens": [{"referenceToken": "the", "heardToken": "the", "startMs": 1000, "endMs": 1140, "vendorConfidence": 0.66, "rawScore": 0.66, "eventClass": "ambiguous"}],
        }
    if caseFamily == "audio_degradation":
        return {
            **base,
            "providerStatus": "invalid_response",
            "unavailableReason": "degraded_audio",
            "tokens": [],
        }
    return {
        **base,
        "providerStatus": "provider_unavailable",
        "unavailableReason": "mock-only fixture",
        "tokens": [],
    }
