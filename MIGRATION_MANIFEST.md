# Migration Manifest

This file records the provenance of the current local ASR evidence package.

| Original path | Destination path | SHA-256 | Decision | Reason | Follow-up |
|---|---|---|---|---|---|
| `C:\Users\oksan\Reader\Manus artifacts\src\reader_leader\policy.py` | `Manus new/src/reader_leader/policy.py` | not computed (reference-only) | adapted | Validated policy logic is reused as the core safety model and renamed to a local package layout | Verify against final source hierarchy |
| `C:\Users\oksan\Reader\Manus artifacts\src\reader_leader\harness.py` | `Manus new/asr-comparison/runner/runBenchmark.py` | not computed | adapted | Existing mock harness structure is useful for synthetic benchmark flow | Rebuild as local package with explicit guard and reports |
| `C:\Users\oksan\Reader\Manus artifacts\src\reader_leader\scorecard.py` | `Manus new/asr-comparison/scorecard/calculateMetrics.py` | not computed | adapted | Scorecard concepts are retained but moved to the new package structure | Validate by tests |
| `C:\Users\oksan\Reader\Manus artifacts\docs\ASR_VENDOR_EVALUATION.md` | `Manus new/docs/ASR_VENDOR_DILIGENCE.md` | not computed | adapted | Existing vendor design notes are reused to create a more explicit diligence checklist | Add current vendor facts and access review |
| `C:\Users\oksan\Reader\Manus artifacts\asr-comparison/report.md` | `Manus new/docs/ASR_ACCEPTANCE_REPORT.md` | not computed | adapted | Historical benchmark summary is used as context only | Replace with final local acceptance report |
| `C:\Users\oksan\Reader\Manus artifacts\PRD.md` | `Manus new/docs/BASELINE_ASSESSMENT.md` | not computed | reference-only | Product requirements are essential for scope but are not a source for a live vendor run | Map to updated safety boundary |
| `C:\Users\oksan\Reader\Files from OneDrive\*` | `Manus new/docs/SOURCE_GAPS.md` | not computed | pending_authoritative_source_review | Exact current authoritative challenge files were not fully confirmed in the local workspace | Human owner to confirm authoritative OneDrive location |
| `C:\Users\oksan\Reader\Manus artifacts\asr-comparison\adapters\mock_adapter.py` | `Manus new/asr-comparison/adapters/mockAdapter.py` | not computed | copied | A safe offline mock adapter is required for deterministic validation | Keep mock-only |

## Notes

- `Manus/` remains read-only and preserved as a baseline.
- `Manus new/` is the only writer-created deliverable folder.
- Actual live vendor execution remains gated until external access, permissions, and retention review are confirmed.
