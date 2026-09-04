export type DataClassification = "synthetic" | "consenting_adult";
export type ProviderId = "speechace" | "soapbox" | "mock";
export type ProviderStatus =
  | "ok"
  | "provider_unavailable"
  | "invalid_response"
  | "rejected_by_guard"
  | "network_disabled";

export type PolicyOutcome = "stay_silent" | "teacher_review" | "analysis_unavailable";

export type TextPassport = {
  textId: string;
  textVersion: string;
  textType: string;
  language: string;
  regionalVariantSetId: string;
  decodabilityOrComplexityReference?: string;
  accessibilityNotes?: string;
  rightsStatus: "unknown" | "draft" | "human_review" | "approved" | "retired";
  visibilityScope: "private_test" | "internal_review";
  workflowStatus: "draft" | "human_review" | "approved";
  reviewerRole?: string;
  approvalTimestamp?: string;
};

export type BenchmarkInput = {
  runId: string;
  testCaseId: string;
  provider: ProviderId;
  sourceDataClassification: DataClassification;
  audioPathOrHandle: string;
  sourceAudioHash: string;
  referenceText: string;
  referenceTokens: string[];
  textPassport: TextPassport;
};

export type NormalizedEvidenceRecord = {
  runId: string;
  testCaseId: string;
  vendor: ProviderId;
  providerStatus: ProviderStatus;
  vendorRequestId?: string;
  modelVersion?: string;
  vendorRegion?: string;
  retentionMode?: string;
  sourceDataClassification: DataClassification;
  sourceAudioHash: string;
  reference: {
    textId: string;
    textVersion: string;
    tokenSequence: string[];
    regionalVariantSetId: string;
  };
  tokens: Array<{
    referenceToken?: string;
    heardToken?: string;
    startMs?: number;
    endMs?: number;
    vendorConfidence?: number;
    rawScore?: number | string;
    alternatives?: string[];
    eventClass?:
      | "exact"
      | "substitution"
      | "omission"
      | "insertion"
      | "self_correction"
      | "ambiguous"
      | "variation"
      | "unknown";
  }>;
  timing: {
    requestStartedAt: string;
    responseReceivedAt?: string;
    endToEndMs?: number;
  };
  policyVersion: string;
  unavailableReason?: string;
};
