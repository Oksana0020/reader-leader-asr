from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from asr_comparison.adapters.mockAdapter import buildMockResponse
from asr_comparison.adapters.vendorAdapter import buildRealVendorResponse, canRunRealProvider
from asr_comparison.runner.inputGuard import validateInputGuard
from src.reader_leader.policy import applyEvidencePolicy


PROVIDERS = ["speechace", "soapbox", "reader_leader_mock"]


def _safe_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": case.get("id", "case-001"),
        "caseFamily": case.get("caseFamily", "exact_known_text"),
        "provider": case.get("provider", "speechace"),
        "sourceDataClassification": case.get("sourceDataClassification", "synthetic"),
        "audioPathOrHandle": case.get("audioPathOrHandle", "synthetic/test.wav"),
        "sourceAudioHash": case.get("sourceAudioHash", "hash"),
        "referenceText": case.get("referenceText", "the river"),
        "referenceTokens": case.get("referenceTokens", ["the", "river"]),
        "runId": case.get("runId", "run-001"),
        "textPassport": {
            "textId": case.get("textPassport", {}).get("textId", "text-001"),
            "textVersion": case.get("textPassport", {}).get("textVersion", "v1"),
            "textType": case.get("textPassport", {}).get("textType", "known_text"),
            "language": case.get("textPassport", {}).get("language", "en-IE"),
            "regionalVariantSetId": case.get("textPassport", {}).get("regionalVariantSetId", "standard"),
            "rightsStatus": case.get("textPassport", {}).get("rightsStatus", "approved"),
            "visibilityScope": case.get("textPassport", {}).get("visibilityScope", "private_test"),
            "workflowStatus": case.get("textPassport", {}).get("workflowStatus", "approved"),
        },
    }


def compareProvidersAgainstPrototype(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in cases:
        normalized = _safe_case(item)
        guard = validateInputGuard({
            **normalized,
            "provider": normalized["provider"],
            "realProviderAttempt": False,
            "serverAuthorised": False,
        })

        if not guard["ok"]:
            rows.append({
                "testCaseId": normalized["id"],
                "provider": normalized["provider"],
                "status": "blocked",
                "policyResult": "analysis_unavailable",
                "reason": guard["violations"][0]["reason"] if guard.get("violations") else "guard_rejected",
            })
            continue

        if normalized["provider"] == "reader_leader_mock":
            response = buildMockResponse(normalized["caseFamily"])
            first_token = response["tokens"][0] if response["tokens"] else {}
            candidate = {
                "targetToken": first_token.get("referenceToken", "unknown"),
                "heardToken": first_token.get("heardToken", "unknown"),
                "confidence": float(first_token.get("vendorConfidence", 0.0) or 0.0),
                "evidence": first_token.get("eventClass", "unknown"),
                "classification": first_token.get("eventClass", "unknown"),
            }
            result = applyEvidencePolicy(candidate)
            rows.append({
                "testCaseId": normalized["id"],
                "provider": "reader_leader_mock",
                "status": "mock_only",
                "policyResult": result["policyAction"],
                "reason": result["policyReason"],
            })
            continue

        if normalized["provider"] == "speechace":
            if not canRunRealProvider("speechace"):
                rows.append({
                    "testCaseId": normalized["id"],
                    "provider": "speechace",
                    "status": "provider_unavailable",
                    "policyResult": "analysis_unavailable",
                    "reason": "Speechace real-run is disabled unless ENABLE_REAL_VENDOR_RUNS=true and local credentials user1/password1 plus allowlist token are set.",
                })
                continue

            response = buildRealVendorResponse("speechace", normalized["caseFamily"])
            first_token = response["tokens"][0] if response["tokens"] else {}
            candidate = {
                "targetToken": first_token.get("referenceToken", "unknown"),
                "heardToken": first_token.get("heardToken", "unknown"),
                "confidence": float(first_token.get("vendorConfidence", 0.0) or 0.0),
                "evidence": first_token.get("eventClass", "unknown"),
                "classification": first_token.get("eventClass", "unknown"),
            }
            result = applyEvidencePolicy(candidate)
            rows.append({
                "testCaseId": normalized["id"],
                "provider": "speechace",
                "status": "live_vendor_eval",
                "policyResult": result["policyAction"],
                "reason": result["policyReason"],
            })
            continue

        if normalized["provider"] == "soapbox":
            if not canRunRealProvider("soapbox"):
                rows.append({
                    "testCaseId": normalized["id"],
                    "provider": "soapbox",
                    "status": "provider_unavailable",
                    "policyResult": "analysis_unavailable",
                    "reason": "SoapBox real-run is disabled unless ENABLE_REAL_VENDOR_RUNS=true and local credentials user1/password1 plus allowlist token are set.",
                })
                continue

            response = buildRealVendorResponse("soapbox", normalized["caseFamily"])
            first_token = response["tokens"][0] if response["tokens"] else {}
            candidate = {
                "targetToken": first_token.get("referenceToken", "unknown"),
                "heardToken": first_token.get("heardToken", "unknown"),
                "confidence": float(first_token.get("vendorConfidence", 0.0) or 0.0),
                "evidence": first_token.get("eventClass", "unknown"),
                "classification": first_token.get("eventClass", "unknown"),
            }
            result = applyEvidencePolicy(candidate)
            rows.append({
                "testCaseId": normalized["id"],
                "provider": "soapbox",
                "status": "live_vendor_eval",
                "policyResult": result["policyAction"],
                "reason": result["policyReason"],
            })
            continue

    return rows


def writeComparisonReport(rows: list[dict[str, Any]], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return output


def main() -> None:
    cases = [
        {
            "id": "exact-001",
            "provider": "reader_leader_mock",
            "caseFamily": "exact_known_text",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture-001.wav",
            "sourceAudioHash": "hash-001",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "runId": "run-001",
            "textPassport": {"textId": "text-001", "textVersion": "v1", "regionalVariantSetId": "standard", "rightsStatus": "approved", "visibilityScope": "private_test", "workflowStatus": "approved"},
        },
        {
            "id": "accent-001",
            "provider": "reader_leader_mock",
            "caseFamily": "accent_dialect_variation",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture-002.wav",
            "sourceAudioHash": "hash-002",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "runId": "run-002",
            "textPassport": {"textId": "text-002", "textVersion": "v1", "regionalVariantSetId": "irish-english", "rightsStatus": "approved", "visibilityScope": "private_test", "workflowStatus": "approved"},
        },
        {
            "id": "speechace-001",
            "provider": "speechace",
            "caseFamily": "exact_known_text",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture-003.wav",
            "sourceAudioHash": "hash-003",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "runId": "run-003",
            "textPassport": {"textId": "text-003", "textVersion": "v1", "regionalVariantSetId": "standard", "rightsStatus": "approved", "visibilityScope": "private_test", "workflowStatus": "approved"},
        },
        {
            "id": "soapbox-001",
            "provider": "soapbox",
            "caseFamily": "exact_known_text",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture-004.wav",
            "sourceAudioHash": "hash-004",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "runId": "run-004",
            "textPassport": {"textId": "text-004", "textVersion": "v1", "regionalVariantSetId": "standard", "rightsStatus": "approved", "visibilityScope": "private_test", "workflowStatus": "approved"},
        },
    ]

    report = compareProvidersAgainstPrototype(cases)
    writeComparisonReport(report, "asr-comparison/results/provider-comparison.json")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
