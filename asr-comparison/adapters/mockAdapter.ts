export type MockEventClass =
  | "exact"
  | "substitution"
  | "omission"
  | "insertion"
  | "self_correction"
  | "ambiguous"
  | "variation"
  | "unknown";

export type MockProviderResponse = {
  vendor: "mock";
  providerStatus: "ok" | "provider_unavailable" | "invalid_response";
  vendorRequestId?: string;
  modelVersion?: string;
  vendorRegion?: string;
  retentionMode?: string;
  tokens: Array<{
    referenceToken?: string;
    heardToken?: string;
    startMs?: number;
    endMs?: number;
    vendorConfidence?: number;
    rawScore?: number | string;
    alternatives?: string[];
    eventClass?: MockEventClass;
  }>;
  timing?: {
    requestStartedAt: string;
    responseReceivedAt?: string;
    endToEndMs?: number;
  };
  policyVersion?: string;
  unavailableReason?: string;
};

export function buildMockResponse(caseFamily: string): MockProviderResponse {
  const base = {
    vendor: "mock" as const,
    providerStatus: "ok" as const,
    vendorRequestId: "mock-request-001",
    modelVersion: "mock-local-v1",
    vendorRegion: "synthetic-test",
    retentionMode: "synthetic-only",
    policyVersion: "RL-0.2-local-synthetic",
    timing: {
      requestStartedAt: "2026-01-01T00:00:00.000Z",
      responseReceivedAt: "2026-01-01T00:00:00.050Z",
      endToEndMs: 50,
    },
  };

  switch (caseFamily) {
    case "exact_known_text":
      return {
        ...base,
        tokens: [{ referenceToken: "the", heardToken: "the", startMs: 120, endMs: 220, vendorConfidence: 0.93, rawScore: 0.93, eventClass: "exact" }],
      };
    case "substitution":
      return {
        ...base,
        tokens: [{ referenceToken: "red", heardToken: "bed", startMs: 300, endMs: 420, vendorConfidence: 0.78, rawScore: 0.78, eventClass: "substitution" }],
      };
    case "omission_insertion":
      return {
        ...base,
        tokens: [{ referenceToken: "river", heardToken: "rive", startMs: 500, endMs: 620, vendorConfidence: 0.74, rawScore: 0.74, eventClass: "omission" }],
      };
    case "self_correction_in_flight":
      return {
        ...base,
        tokens: [
          { referenceToken: "rain", heardToken: "reign", startMs: 700, endMs: 830, vendorConfidence: 0.75, rawScore: 0.75, eventClass: "self_correction" },
          { referenceToken: "rain", heardToken: "rain", startMs: 850, endMs: 980, vendorConfidence: 0.91, rawScore: 0.91, eventClass: "exact" },
        ],
      };
    case "hesitation_pause":
      return {
        ...base,
        providerStatus: "ok",
        tokens: [{ referenceToken: "the", heardToken: "the", startMs: 1000, endMs: 1140, vendorConfidence: 0.66, rawScore: 0.66, eventClass: "ambiguous" }],
      };
    case "accent_dialect_variation":
      return {
        ...base,
        tokens: [{ referenceToken: "cat", heardToken: "kat", startMs: 1200, endMs: 1350, vendorConfidence: 0.81, rawScore: 0.81, eventClass: "variation" }],
      };
    case "ambiguous_near_homophone":
      return {
        ...base,
        tokens: [{ referenceToken: "their", heardToken: "there", startMs: 1400, endMs: 1540, vendorConfidence: 0.7, rawScore: 0.7, eventClass: "ambiguous" }],
      };
    case "audio_degradation":
      return {
        ...base,
        providerStatus: "invalid_response",
        unavailableReason: "degraded_audio",
        tokens: [],
      };
    default:
      return {
        ...base,
        providerStatus: "provider_unavailable",
        unavailableReason: "mock-only fixture",
        tokens: [],
      };
  }
}
