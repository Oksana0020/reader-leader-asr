# Reader Leader ASR Evaluation — Acceptance Report

## Executive status

The local implementation is a mock-only, privacy-safe synthetic evaluation environment. It preserves the key Reader Leader policy boundary: low confidence, accent and dialect variation, pause/hesitation, ambiguity and other uncertain evidence do not permit automatic child-facing corrections. Live vendor execution remains disabled until current access and retention approval are verified.

## Work completed in Manus new

- Created the new writable working package and source inventory
- Reused the validated policy and synthetic harness design from `Manus artifacts`
- Implemented a deterministic policy function and local privacy guard
- Added a mock provider and offline benchmark flow
- Created minimal tests proving the safety gate and policy logic
- Documented current scope, gaps and remaining approvals

## Source inventory and reconciliation decisions

- `Manus artifacts` is retained as the validated read-only baseline.
- OneDrive challenge materials were reviewed only as provisional context because the authoritative current root could not be confirmed during the local inspection.
- The current implementation keeps the most reliable local safety logic and synthetic harness design, while marking real vendor actions as pending source review and explicit approval.

## Reused / adapted / excluded baseline work

- Reused: policy logic, benchmark design, false-correction framing
- Adapted: package structure and source inventory to the new target layout
- Excluded: live network calls, real API assumptions, and any child-data processing

## Architecture and current mode

- Local mock benchmark only
- no `.env` values committed
- real vendor mode disabled by default
- all vendor output normalized before policy use

## Safety and privacy conformance table

| Condition | Result |
|---|---|
| Confidence < 0.72 | stay_silent |
| accent/dialect/regional variation | stay_silent |
| ambiguity / near-homophone | stay_silent |
| pause / degraded audio | stay_silent |
| possible substitution or omission | teacher_review |
| self-correction in flight | teacher_review, no final error |
| malformed provider payload | analysis_unavailable |
| learner / school / consent identifiers | rejected before provider call |
| unapproved text rights or visibility | rejected |

## Test and build evidence

Command run:

```bash
cd "c:\Users\oksan\Reader\Manus new"
python -m unittest discover -s tests -v
```

Current result: 5 tests passed after import and guard fixes. The package remains offline and mock-only.

## Mock benchmark results

The mock benchmark validates the offline plumbing and policy behavior. This is not vendor performance evidence and must not be interpreted as a live ASR quality claim.

## Provider status

- Speechace: scaffolded, disabled until authorised synthetic-run conditions are satisfied
- SoapBox / Curriculum Associates: provider unavailable / pending current access review
- Mock mode: working offline

## Required approvals before real vendor use

- valid non-production Speechace key
- explicit project owner approval for synthetic run
- retention or zero-retention confirmation
- region selection and account ownership recorded
- rights-cleared text approval for private-test use

## Known limitations and roadmap exclusions

- no live network benchmark execution yet
- no child-data / production audio usage
- no learning-gain, diagnosis or placement claims
- no broad multilingual or public content rollout

## Remaining blockers and exact owner actions

- Confirm the current authoritative OneDrive challenge source location.
- Confirm current Speechace access and privacy terms.
- Confirm SoapBox / Curriculum Associates current evaluation access.

## Suggested team review order

1. Safety policy and privacy guard
2. Mock benchmark and scorecard plumbing
3. Vendor diligence and transition plan
4. Only then: real authorised synthetic run
