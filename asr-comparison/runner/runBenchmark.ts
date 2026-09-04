import { buildMockResponse } from "../adapters/mockAdapter";
import { validateInputGuard } from "./inputGuard";

export type BenchmarkCase = {
  id: string;
  caseFamily: string;
  expectedPolicyOutcome: string;
  referenceTokens: string[];
  referenceText: string;
  timingBounds?: { minMs: number; maxMs: number };
  sourceDataClassification: "synthetic" | "consenting_adult";
  audioPathOrHandle: string;
  sourceAudioHash: string;
  provider: "speechace" | "soapbox" | "mock";
  runId: string;
  textPassport: {
    textId: string;
    textVersion: string;
    textType: string;
    language: string;
    regionalVariantSetId: string;
    rightsStatus: "approved";
    visibilityScope: "private_test";
    workflowStatus: "approved";
  };
};

export function runBenchmark(cases: BenchmarkCase[]) {
  const results: Record<string, unknown>[] = [];

  for (const item of cases) {
    const guard = validateInputGuard({
      ...item,
      provider: "mock",
      realProviderAttempt: false,
      serverAuthorised: false,
    });

    if (!guard.ok) {
      results.push({
        testCaseId: item.id,
        status: "blocked",
        reason: guard.violations[0]?.reason ?? "guard_rejected",
      });
      continue;
    }

    const providerResponse = buildMockResponse(item.caseFamily);
    results.push({
      testCaseId: item.id,
      caseFamily: item.caseFamily,
      expectedPolicyOutcome: item.expectedPolicyOutcome,
      provider: item.provider,
      providerStatus: providerResponse.providerStatus,
      tokens: providerResponse.tokens,
      timing: providerResponse.timing,
      vendor: providerResponse.vendor,
    });
  }

  return results;
}
