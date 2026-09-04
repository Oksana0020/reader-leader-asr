from __future__ import annotations

import json
from pathlib import Path

from asr_comparison.adapters.mockAdapter import buildMockResponse
from asr_comparison.runner.inputGuard import validateInputGuard


def runBenchmark(cases: list[dict]) -> list[dict]:
    results: list[dict] = []
    for case in cases:
        guard = validateInputGuard({
            **case,
            "provider": "mock",
            "realProviderAttempt": False,
            "serverAuthorised": False,
        })
        if not guard["ok"]:
            results.append({
                "testCaseId": case.get("id"),
                "status": "blocked",
                "reason": guard["violations"][0]["reason"] if guard.get("violations") else "guard_rejected",
            })
            continue

        response = buildMockResponse(case.get("caseFamily", "exact_known_text"))
        results.append({
            "testCaseId": case.get("id"),
            "caseFamily": case.get("caseFamily"),
            "expectedPolicyOutcome": case.get("expectedPolicyOutcome"),
            "providerStatus": response["providerStatus"],
            "tokens": response["tokens"],
            "vendor": response["vendor"],
            "timing": response["timing"],
        })
    return results


def main() -> None:
    fixtures = [
        {
            "id": "exact-001",
            "caseFamily": "exact_known_text",
            "expectedPolicyOutcome": "teacher_review",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture-001.wav",
            "sourceAudioHash": "hash-001",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "runId": "run-001",
            "textPassport": {
                "textId": "text-001",
                "textVersion": "v1",
                "regionalVariantSetId": "standard",
                "rightsStatus": "approved",
                "visibilityScope": "private_test",
                "workflowStatus": "approved",
            },
        },
        {
            "id": "accent-001",
            "caseFamily": "accent_dialect_variation",
            "expectedPolicyOutcome": "stay_silent",
            "sourceDataClassification": "synthetic",
            "audioPathOrHandle": "synthetic/fixture-002.wav",
            "sourceAudioHash": "hash-002",
            "referenceText": "the river",
            "referenceTokens": ["the", "river"],
            "runId": "run-002",
            "textPassport": {
                "textId": "text-002",
                "textVersion": "v1",
                "regionalVariantSetId": "irish-english",
                "rightsStatus": "approved",
                "visibilityScope": "private_test",
                "workflowStatus": "approved",
            },
        },
    ]
    output = runBenchmark(fixtures)
    Path("asr-comparison/results").mkdir(parents=True, exist_ok=True)
    Path("asr-comparison/results/mock-benchmark.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
