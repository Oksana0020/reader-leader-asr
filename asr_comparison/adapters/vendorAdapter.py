from __future__ import annotations

import os
from typing import Any


def _env_bool(name: str) -> bool:
    return str(os.getenv(name, "")).strip().lower() in {"1", "true", "yes", "on"}


def _normalize_provider(provider: str) -> str:
    return (provider or "").strip().lower()


def canRunRealProvider(provider: str) -> bool:
    provider_name = _normalize_provider(provider)
    if provider_name not in {"speechace", "soapbox"}:
        return False

    if not _env_bool("ENABLE_REAL_VENDOR_RUNS"):
        return False

    if not os.getenv("ASR_VENDOR_ALLOWLIST_TOKEN", "").strip():
        return False

    username = os.getenv("ASR_LOCAL_TEST_USERNAME", "").strip()
    password = os.getenv("ASR_LOCAL_TEST_PASSWORD", "").strip()
    if username != "user1" or password != "password1":
        return False

    return True


def buildRealVendorResponse(provider: str, case_family: str) -> dict[str, Any]:
    provider_name = _normalize_provider(provider)
    if not canRunRealProvider(provider_name):
        return {
            "vendor": provider_name,
            "providerStatus": "provider_unavailable",
            "unavailableReason": "real provider path disabled or not authorised for this environment",
            "tokens": [],
        }

    if provider_name == "speechace":
        return {
            "vendor": "speechace",
            "providerStatus": "ok",
            "vendorRequestId": "speechace-local-test-request",
            "modelVersion": "speechace-local-test",
            "vendorRegion": os.getenv("SPEECHACE_REGION", "local-test"),
            "retentionMode": os.getenv("SPEECHACE_RETENTION_MODE", "private_test"),
            "policyVersion": "RL-0.2-local-synthetic",
            "timing": {"requestStartedAt": "2026-01-01T00:00:00.000Z", "responseReceivedAt": "2026-01-01T00:00:00.200Z", "endToEndMs": 200},
            "tokens": [{"referenceToken": "the", "heardToken": "the", "startMs": 100, "endMs": 200, "vendorConfidence": 0.93, "rawScore": 0.93, "eventClass": "exact"}],
        }

    return {
        "vendor": "soapbox",
        "providerStatus": "ok",
        "vendorRequestId": "soapbox-local-test-request",
        "modelVersion": "soapbox-local-test",
        "vendorRegion": os.getenv("SOAPBOX_REGION", "local-test"),
        "retentionMode": os.getenv("SOAPBOX_RETENTION_MODE", "private_test"),
        "policyVersion": "RL-0.2-local-synthetic",
        "timing": {"requestStartedAt": "2026-01-01T00:00:00.000Z", "responseReceivedAt": "2026-01-01T00:00:00.220Z", "endToEndMs": 220},
        "tokens": [{"referenceToken": "the", "heardToken": "the", "startMs": 100, "endMs": 220, "vendorConfidence": 0.91, "rawScore": 0.91, "eventClass": "exact"}],
    }
