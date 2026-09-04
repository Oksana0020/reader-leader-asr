# Source of Truth and Requirements Reconciliation

Date: 2026-08-27

## Source inventory

| Source | Path | Status | Notes |
|---|---|---|---|
| Local project workspace | `C:\Users\oksan\Reader` | present | contains `Manus artifacts` and relevant challenge materials |
| Existing validated baseline | `C:\Users\oksan\Reader\Manus artifacts` | present | read-only historical baseline |
| OneDrive challenge materials | `C:\Users\oksan\Reader\Files from OneDrive` | partial | available but not confirmed as the current authoritative source root |
| Target implementation folder | `C:\Users\oksan\Reader\Manus new` | created | writable delivery package |

## Hierarchy used for this implementation

1. Latest National AI Challenge participant playbook (if available locally)
2. Reader Leader challenge statement / safety boundary materials
3. Methodology, student journey and library materials
4. Existing validated `Manus artifacts` ASR comparison and policy work
5. Historical PDFs, screenshots and exported notes only as context

## Requirements table

| Requirement | Source | Decision |
|---|---|---|
| Teacher-governed oral-reading evidence workflow | challenge statement + product docs | implemented as policy-first architecture |
| Deterministic safety policy | validated baseline | retained and enforced locally |
| Synthetic-only vendor comparison | ASR benchmark design docs | implemented as default mode |
| No live vendor run without approval | challenge / safety docs | enforced by real-run gate |
| Speechace ready for authorised synthetic shadow run | vendor docs + design | scaffolded, disabled until credentials and verification |
| SoapBox / Curriculum Associates not treated as live | vendor diligence docs | provider unavailable status retained |
| Roadmap-only features excluded | methodology / roadmap docs | documented as excluded |

## Conflict log

| Source path | Current requirement | Older inconsistent requirement | Final decision | Code impact | Doc impact | Status |
|---|---|---|---|---|---|---|
| `Files from OneDrive` | authoritative challenge root must be confirmed | local guess-work is not safe | pending source review | none yet | documented in gaps | pending source review |
| `Manus artifacts` ASR comparison | synthetic benchmark for safe local validation | live vendor winner claims are not in scope | keep synthetic-only, mock-first | local harness and offline tests | required docs updated | implemented |
| current vendor docs | real vendor evaluation requires account and retention approval | historical docs alone are not enough | treat as unavailable unless explicit approval exists | gate logic added | diligence checklist added | implemented |

## Decision summary

This implementation uses the validated `Manus artifacts` ASR and policy baseline as the strongest available local source, while keeping the project explicitly synthetic-only until a current authoritative source and real-vendor approval are confirmed.
