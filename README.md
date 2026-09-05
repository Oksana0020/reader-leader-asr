# Reader Leader ASR Evaluation

Reader Leader is an AI-supported reading platform designed to help children develop reading fluency and comprehension with teacher oversight and parent support.

This repository contains the **Automatic Speech Recognition (ASR) evaluation and safety layer** of Reader Leader. It evaluates how spoken reading evidence should be interpreted before any feedback is presented to a child.

The guiding product principle is simple:

> **Reader Leader knows when not to correct.**

A child’s pronunciation should not be labelled as incorrect simply because an ASR system is uncertain, unfamiliar with an accent or dialect, or has incomplete evidence. When the evidence is weak or ambiguous, the system should prefer **silence or teacher review** rather than generating a potentially incorrect child-facing correction.

---

## Product Intent

Reader Leader uses AI to support reading practice while keeping teachers in control of important decisions.

The ASR evaluation component is designed around four principles:

* **Gather evidence without forcing a correction.**
* **Avoid child-facing corrections when ASR confidence or evidence is insufficient.**
* **Escalate potentially meaningful but uncertain cases for teacher review.**
* **Validate the decision policy locally before allowing controlled live-provider evaluation.**

The objective is not simply to identify differences between a child's speech and a reference transcript. The objective is to determine whether the available evidence is **strong enough to justify an intervention**.

---

## Decision Policy

The current policy has three primary outcomes.

### `stay_silent`

The system does not provide a correction when the evidence is ambiguous, weak, or potentially explained by legitimate speech variation such as accent or dialect.

This is an intentional safety behaviour, not a failure.

### `teacher_review`

The system escalates a case when the evidence indicates a possible reading error but does not meet the criteria for a safe automatic correction.

The teacher remains responsible for deciding whether intervention is appropriate.

### `analysis_unavailable`

The system does not make a decision when provider output is malformed, incomplete, or otherwise unsuitable for analysis.

Instead of guessing, the system rejects the evidence.

This creates a deliberate hierarchy:

**Reliable evidence → appropriate action**

**Uncertain evidence → silence or teacher review**

**Invalid evidence → reject**

---

## Where This Fits in Reader Leader

The wider Reader Leader platform supports a teacher-governed reading workflow:

```text
Teacher uploads reading material
              ↓
       AI prepares activities
              ↓
       Child selects a story
              ↓
         Child reads aloud
              ↓
        ASR captures evidence
              ↓
       Evidence is evaluated
              ↓
   ┌──────────┼──────────────┐
   ↓          ↓              ↓
Stay silent  Teacher review  Invalid evidence
   ↓          ↓              ↓
Continue      Teacher        Reject
reading       decides        analysis
              ↓
        Reading report
              ↓
     Teacher / parent view
```

This repository focuses specifically on the **ASR evidence evaluation stage**.

It does not attempt to replace teacher judgement.

---

## What Is in This Repository

The repository contains the local evaluation harness and policy logic used to test the ASR behaviour:

### `src/reader_leader/policy.py`

Contains the evidence policy that determines whether an ASR result should:

* remain silent,
* be escalated for teacher review, or
* be rejected as unavailable or invalid.

### `asr_comparison/runner/compareProviders.py`

Contains the provider comparison flow used to run benchmark cases against the supported prototype/provider behaviours.

### `asr_comparison/adapters/vendorAdapter.py`

Contains the environment-gated adapter used for controlled live-provider evaluation.

Live provider execution is not the default path.

### `asr_comparison/runner/inputGuard.py`

Provides validation checks intended to prevent unsafe learner data and malformed benchmark payloads from entering the evaluation flow.

### `tests/`

Contains regression tests covering the policy and input-guard behaviour.

### `asr-comparison/results/`

Contains generated benchmark outputs, including:

* CSV results,
* Markdown summaries,
* SVG visualisations.

---

## Safety-First Benchmark Design

The evaluation harness is intentionally designed to avoid false confidence.

An ASR result should only influence the Reader Leader policy when the evidence is sufficiently complete, correctly normalized, and compatible with the decision rules.

The benchmark therefore includes controls for:

* invalid learner data,
* malformed input,
* unauthorized or unexpected files,
* incomplete provider output,
* provider-output normalization,
* explicit environment gates for live-provider evaluation, and
* traceable benchmark results.

The purpose of these controls is to make the evaluation process reproducible and auditable rather than relying on individual examples or subjective interpretation.

---

## Handling Speech Variation

Children may speak with different accents, dialects, speech patterns, and pronunciation characteristics.

An ASR mismatch is therefore **not automatically treated as a reading error**.

For example, if the available evidence does not allow the system to distinguish confidently between:

* a genuine reading error,
* an accent-related difference,
* a dialect variation,
* an ASR recognition error, or
* insufficient audio evidence,

the safer outcome is to avoid an automatic child-facing correction.

This is a core design decision of Reader Leader.

---

## Local Validation

The project includes a unit test suite for validating the policy and input-guard behaviour.

From PowerShell:

```powershell
cd "c:\Users\oksan\Reader\ASR"
$env:PYTHONPATH = "."
python -m unittest discover -s tests -v
```

The test suite is intended to verify that the implemented decision rules continue to behave as expected as the evaluation harness develops.

---

## Real-Provider Evaluation Gate

Live vendor execution is intentionally disabled by default.

Real-provider evaluation should only be enabled when the required environment configuration has been explicitly set for controlled local testing.

Example configuration using placeholders:

```dotenv
ENABLE_REAL_VENDOR_RUNS=true
ASR_VENDOR_ALLOWLIST_TOKEN=<approved-token>
ASR_LOCAL_TEST_USERNAME=<local-test-user>
ASR_LOCAL_TEST_PASSWORD=<local-test-password>
```

These values are placeholders only.

**Real credentials, API keys, tokens, passwords, or learner data must never be committed to the repository.**

The environment gate provides a separation between:

1. deterministic local benchmarking, and
2. controlled evaluation using an external ASR provider.

This helps keep development and benchmark runs reproducible while reducing the risk of unintentionally sending data to a live provider.

---

## Benchmark Scenarios

The evaluation outputs cover different types of reading evidence, including scenarios such as:

* exact transcript matches,
* potential reading differences,
* accent variation,
* ambiguous provider signals,
* incomplete provider analysis, and
* invalid or malformed evidence.

The purpose of these scenarios is to evaluate the **decision behaviour**, not simply to maximise an ASR accuracy score.

A high recognition rate alone does not demonstrate that an educational reading system is safe to use.

---

## Evaluation Philosophy

Traditional ASR evaluation often focuses on metrics such as recognition accuracy or Word Error Rate.

Reader Leader adds a product-level question:

> **Even when the ASR detects a difference, should the system actually correct the child?**

This distinction is important because an ASR system can produce an incorrect or overconfident interpretation.

Reader Leader therefore evaluates both:

**What did the ASR system report?**

and

**What should the product do with that evidence?**

The second question is governed by the Reader Leader policy.

---

## Traceability

Benchmark results are generated in:

```text
asr-comparison/results/
```

The available outputs can be used to inspect and communicate the results of different evidence scenarios.

The intended workflow is:

```text
Input
  ↓
Validation
  ↓
Provider output
  ↓
Normalization
  ↓
Evidence policy
  ↓
Decision
  ↓
Benchmark result
```

This makes it possible to inspect how an input reached its final policy outcome.

---

## Limitations

This repository is an evaluation harness, not a complete clinical, diagnostic, or educational assessment system.

The benchmark should not be interpreted as proof that an ASR provider is universally accurate for every child, accent, dialect, age group, recording environment, or reading ability.

In particular:

* benchmark cases are limited representations of real-world reading,
* ASR performance can vary between providers and environments,
* speech variation cannot always be reliably distinguished from reading errors,
* local benchmark performance does not guarantee real-world performance, and
* teacher review remains important for uncertain cases.

The system is deliberately designed to avoid presenting uncertainty as certainty.

---

## Future Evaluation

Potential future work includes:

* expanding the benchmark dataset,
* evaluating additional accents and dialects,
* testing a wider range of children's reading scenarios,
* comparing multiple ASR providers under the same policy,
* measuring false-correction and missed-error rates,
* evaluating background-noise conditions,
* improving teacher-review workflows, and
* validating the policy against appropriately governed real-world data.

Any evaluation involving real children's data should follow the appropriate privacy, consent, safeguarding, and data-governance requirements.

---

## Summary

Reader Leader is designed around a simple safety principle:

> **Do not turn uncertain ASR evidence into a confident correction.**

The ASR evaluation layer therefore distinguishes between evidence that can support an action, evidence that requires teacher judgement, and evidence that should be rejected.

The core behaviours are:

```text
Strong evidence
      ↓
 Appropriate action

Uncertain evidence
      ↓
 Silence / Teacher review

Invalid evidence
      ↓
 Reject analysis
```

The result is a **local-first, teacher-governed evaluation environment** designed to test whether ASR evidence can be used responsibly within a children's reading platform.

The goal is not to make the system correct every perceived pronunciation difference.

The goal is to make sure that when Reader Leader does intervene, the evidence is strong enough to justify doing so.
