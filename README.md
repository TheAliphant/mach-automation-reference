# MACH reference: n8n lead triage

A small, credential-free reference workflow showing how MACH structures bounded n8n delivery.

## Problem

Receive a lead through a webhook, normalize unreliable input, classify priority with explicit rules, and return a structured response that downstream systems can route safely.

## Flow

`Webhook → Normalize + classify (Code) → Respond to Webhook`

The reference deliberately uses deterministic classification instead of an external LLM so it can be imported and tested without credentials. In a production build, the classifier can be replaced or augmented with OpenAI/Claude while preserving the same structured output contract and fallback rules.

## Input

POST JSON to the webhook:

```json
{
  "name": "Ada Example",
  "email": "ada@example.com",
  "company": "Example Ltd",
  "message": "We need an automation this week",
  "budget": 2500
}
```

## Output contract

```json
{
  "ok": true,
  "lead": {
    "name": "Ada Example",
    "email": "ada@example.com",
    "company": "Example Ltd"
  },
  "triage": {
    "priority": "high",
    "reason": "budget_and_urgency"
  }
}
```

## Acceptance checks

1. Missing optional fields never crash the workflow.
2. Invalid email is flagged instead of silently accepted.
3. Classification is deterministic and explainable.
4. Output shape stays stable for CRM/Sheets/Slack downstream steps.
5. No credentials or private customer data are embedded in the workflow export.

## Import

Import `workflow.json` into n8n, open the Webhook node, run a test execution and POST one of the payloads from `test-payloads.json`.

This is a reference implementation, not a claim of prior client work.
