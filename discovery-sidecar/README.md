# MACH Discovery Sidecar

Independent agent-discovery and communication laboratory for MACH.

## Non-negotiable isolation

This directory is intentionally **not connected to MACH production**.

- No imports from the MACH production repository.
- No production endpoints.
- No production credentials or wallets.
- No outbound network calls in runtime code.
- No writes to production.
- `/v1/execute` is hard-disabled.
- All sample capabilities are prefixed `lab.mock.`.
- Deleting this directory has zero effect on MACH production.

The sidecar exists to test **how agents discover, describe, compare and communicate about capabilities** before any production integration is considered.

## What is implemented

- Discovery Edge: capability catalog, agent-facing metadata, `llms.txt`, `agents.txt`, OpenAPI scaffold.
- MACH Service Agent shell: discover, describe/quote, sandbox probe, feedback.
- A2A-ready Agent Card scaffold (not advertised as protocol-conformant until tested).
- Agent Lab prompt generator for Claude, OpenAI, Google ADK/Gemini, AWS Strands, CrewAI and Cline.
- Telemetry schema for discovery → probe → quote → purchase/execution outcomes.
- Strict local sandbox and rate limits.
- Communication plan and Agent Challenge assets.
- Isolation tests that reject production connectivity.

## Run locally

```bash
cd discovery-sidecar
python3 sidecar.py
```

Then:

```bash
curl http://127.0.0.1:8787/health
curl "http://127.0.0.1:8787/v1/discover?task=normalize%20json"
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Generate Agent Lab prompts without calling any model/API:

```bash
python3 lab/runner.py
```

## Safety state

Current mode: **LAB_ONLY / PRODUCTION_DISCONNECTED**

Nothing in this sidecar can execute a real MACH capability.
