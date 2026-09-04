# Implementation Plan

## Completed

1. Create clean working area under `Manus new/`
2. Document source inventory and decision hierarchy
3. Reuse policy logic and scorecard ideas from validated baseline
4. Build deterministic policy and safety gate logic
5. Add offline mock provider, benchmark fixtures and runner
6. Add local tests proving offline safety and mock flow
7. Produce documentation and acceptance report placeholders

## Remaining dependency gates

- current authoritative OneDrive source root confirmation
- Speechace non-production account access and retention approval
- SoapBox / Curriculum Associates access confirmation
- rights-cleared text approval for live synthetic runs

## Roadmap exclusions

- broad learner routing
- diagnosis, placement or learning-gain claims
- multilingual production roll-out
- child-data benchmark claims
- live vendor winner selection without explicit approvals

## Current status

The local implementation is complete and tested in mock mode. Real-vendor execution is intentionally disabled and protected by a machine-readable gate.
