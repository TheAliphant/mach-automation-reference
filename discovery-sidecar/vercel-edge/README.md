# MACH Agent Lab Edge

A stateless, publicly callable A2A 1.0 discovery edge.

## Isolation

This project contains:
- no imports from MACH production;
- no MACH production URLs;
- no wallet/payment code;
- no secrets;
- no persistence requirement;
- only `lab.mock.*` fixtures.

Production execution is explicitly unavailable and `POST /api/execute` always returns HTTP 503.

## External verification

After deployment:

```bash
curl -fsS https://<host>/.well-known/agent-card.json | jq .
curl -fsS -H 'Content-Type: application/json' \
  --data @a2a-request.example.json \
  https://<host>/api/a2a/message:send | jq .
```

The second command must return `message.role == "ROLE_AGENT"` and `productionConnected == false`.
