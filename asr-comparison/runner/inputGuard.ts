export type GuardViolation = {
  reason: string;
  field: string;
};

export function validateInputGuard(input: Record<string, any>): { ok: true } | { ok: false; violations: GuardViolation[] } {
  const violations: GuardViolation[] = [];

  const forbidden = [
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
  ];

  for (const key of forbidden) {
    if (input[key] && String(input[key]).trim() !== "") {
      violations.push({ reason: "personal or school identifier present", field: key });
    }
  }

  if (input.sourceDataClassification && !["synthetic", "consenting_adult"].includes(input.sourceDataClassification)) {
    violations.push({ reason: "unsupported classification", field: "sourceDataClassification" });
  }

  const textPassport = input.textPassport ?? {};
  if (!textPassport.textId || !textPassport.textVersion || !textPassport.regionalVariantSetId) {
    violations.push({ reason: "text passport is incomplete", field: "textPassport" });
  }
  if (textPassport.rightsStatus !== "approved") {
    violations.push({ reason: "text not approved for private test use", field: "textPassport.rightsStatus" });
  }
  if (textPassport.visibilityScope !== "private_test") {
    violations.push({ reason: "text visibility scope is not private_test", field: "textPassport.visibilityScope" });
  }

  if (!input.runId || !input.sourceAudioHash || !input.referenceText || !Array.isArray(input.referenceTokens) || input.referenceTokens.length === 0) {
    violations.push({ reason: "benchmark input is missing required metadata", field: "benchmark_input" });
  }

  if (!input.audioPathOrHandle || !String(input.audioPathOrHandle).startsWith("synthetic/")) {
    violations.push({ reason: "audio source is not synthetic and approved for local benchmark use", field: "audioPathOrHandle" });
  }

  if (input.provider && !["speechace", "soapbox", "mock"].includes(input.provider)) {
    violations.push({ reason: "unsupported provider selection", field: "provider" });
  }

  if (input.realProviderAttempt === true && !input.serverAuthorised) {
    violations.push({ reason: "provider call attempted without server-side authorisation", field: "serverAuthorised" });
  }

  if (violations.length > 0) {
    return { ok: false, violations };
  }

  return { ok: true };
}
