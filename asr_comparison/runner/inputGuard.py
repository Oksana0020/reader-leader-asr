from __future__ import annotations

from typing import Any


def validateInputGuard(input: dict[str, Any]) -> dict[str, Any]:
    violations: list[dict[str, str]] = []

    forbidden = [
        "learnerId",
        "studentNumber",
        "childName",
        "school",
        "class",
        "organization",
        "organisation",
        "consentIdentifier",
        "parentEmail",
        "teacherEmail",
        "email",
    ]

    for key in forbidden:
        if input.get(key) not in (None, "", False):
            violations.append({"reason": "personal or school identifier present", "field": key})

    if input.get("sourceDataClassification") not in (None, "synthetic", "consenting_adult"):
        violations.append({"reason": "unsupported classification", "field": "sourceDataClassification"})

    textPassport = input.get("textPassport") or {}
    if not textPassport.get("textId") or not textPassport.get("textVersion") or not textPassport.get("regionalVariantSetId"):
        violations.append({"reason": "text passport is incomplete", "field": "textPassport"})
    if textPassport.get("rightsStatus") != "approved":
        violations.append({"reason": "text not approved for private test use", "field": "textPassport.rightsStatus"})
    if textPassport.get("visibilityScope") != "private_test":
        violations.append({"reason": "text visibility scope is not private_test", "field": "textPassport.visibilityScope"})

    if not input.get("runId") or not input.get("sourceAudioHash") or not input.get("referenceText") or not isinstance(input.get("referenceTokens"), list) or len(input.get("referenceTokens") or []) == 0:
        violations.append({"reason": "benchmark input is missing required metadata", "field": "benchmark_input"})

    audio = str(input.get("audioPathOrHandle") or "")
    if not audio.startswith("synthetic/"):
        violations.append({"reason": "audio source is not synthetic and approved for local benchmark use", "field": "audioPathOrHandle"})

    if input.get("provider") not in (None, "speechace", "soapbox", "mock", "reader_leader_mock"):
        violations.append({"reason": "unsupported provider selection", "field": "provider"})

    if input.get("realProviderAttempt") is True and not input.get("serverAuthorised"):
        violations.append({"reason": "provider call attempted without server-side authorisation", "field": "serverAuthorised"})

    if violations:
        return {"ok": False, "violations": violations}
    return {"ok": True}
