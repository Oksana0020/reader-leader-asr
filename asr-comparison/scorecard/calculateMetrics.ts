export type MetricSummary = {
  total: number;
  byCaseFamily: Record<string, number>;
  statuses: Record<string, number>;
  falseCorrectionCandidates: number;
};

export function calculateMetrics(results: Array<Record<string, any>>): MetricSummary {
  const byCaseFamily: Record<string, number> = {};
  const statuses: Record<string, number> = {};

  for (const result of results) {
    const caseFamily = String(result.caseFamily ?? "unknown");
    byCaseFamily[caseFamily] = (byCaseFamily[caseFamily] ?? 0) + 1;

    const status = String(result.providerStatus ?? "not_run");
    statuses[status] = (statuses[status] ?? 0) + 1;
  }

  return {
    total: results.length,
    byCaseFamily,
    statuses,
    falseCorrectionCandidates: results.filter((result) => {
      const caseFamily = String(result.caseFamily ?? "");
      return ["accent_dialect_variation", "ambiguous_near_homophone", "hesitation_pause", "audio_degradation"].includes(caseFamily);
    }).length,
  };
}
