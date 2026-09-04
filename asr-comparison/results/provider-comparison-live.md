# Reader Leader ASR comparison report

## Run context

- Local test mode enabled via env-backed vendor gate.
- Reader Leader mock remains the safety-first baseline.
- Speechace and SoapBox are evaluated only when the local test credential gate is enabled.

## Results

| Test case | Provider | Status | Policy result | Reason |
| --- | --- | --- | --- | --- |
| exact-001 | reader_leader_mock | mock_only | teacher_review | The supplied provider evidence is not safe for automatic child-facing action. |
| accent-001 | reader_leader_mock | mock_only | stay_silent | The evidence may reflect accent, dialect, or legitimate variation; the safe result is silence. |
| speechace-001 | speechace | live_vendor_eval | teacher_review | The supplied provider evidence is not safe for automatic child-facing action. |
| soapbox-001 | soapbox | live_vendor_eval | teacher_review | The supplied provider evidence is not safe for automatic child-facing action. |
