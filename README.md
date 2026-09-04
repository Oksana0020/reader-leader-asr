# Reader Leader ASR Evaluation Environment

This workspace is the safe, local-only implementation package for Reader Leader ASR comparison work.

## Current scope

- Deterministic evidence policy remains the authority over any child-facing action.
- Local benchmark harness runs in mock mode only.
- Speechace is scaffolded for authorised synthetic use only.
- SoapBox / Curriculum Associates is present as a provider interface with a safe unavailable status until current access is confirmed.
- No real vendor requests are permitted unless server-side authorisation, synthetic-evaluation permission, and retention controls are explicitly satisfied.

## Safe defaults

- No `.env` file is committed.
- No real API keys are required for the default offline run.
- Real-provider mode is disabled by default.
- All provider output is normalized before policy evaluation.

## Quick start

```bash
cd "c:\Users\oksan\Reader\Manus new"
python -m unittest discover -s tests -v
```

or, if the project is used via Node tooling in a later iteration:

```bash
cd "c:\Users\oksan\Reader\Manus new"
node --test
```

## Environment variables

For a local test-only real-vendor run, set the following values exactly.

```dotenv
SPEECHACE_API_KEY=
SPEECHACE_REGION=local-test
SPEECHACE_RETENTION_MODE=private_test
SPEECHACE_TEST_ACCOUNT_OWNER=approved
SOAPBOX_API_KEY=
SOAPBOX_REGION=local-test
SOAPBOX_RETENTION_MODE=private_test
SOAPBOX_TEST_ACCOUNT_OWNER=approved
ENABLE_REAL_VENDOR_RUNS=true
ASR_VENDOR_ALLOWLIST_TOKEN=approved
ASR_LOCAL_TEST_USERNAME=user1
ASR_LOCAL_TEST_PASSWORD=password1
```

## Required status

The default benchmark remains mock-only and offline unless this explicit local test gate is enabled. The real-vendor path is intentionally blocked until both the provider approval flag and the local test credentials are present.
