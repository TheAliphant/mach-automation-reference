# A2A 1.0 Lab Adapter

Public Agent Card:
https://mach-agent-lab-xqjtq9.v2.appdeploy.ai/.well-known/agent-card.json

Preferred interface:
- URL: https://mach-agent-lab-xqjtq9.v2.appdeploy.ai/api/a2a
- Binding: HTTP+JSON
- Protocol version: 1.0

Implemented operation:
- POST `/api/a2a/message:send` — synchronous SendMessage for discovery research.

The adapter returns `SendMessageResponse.message` with `ROLE_AGENT`.

Not advertised:
- streaming
- push notifications
- paid execution
- production tasks
- wallets
- MACH production capabilities

This is deliberately a narrow agent-to-agent discovery surface. It exists to collect real external-agent discovery behavior without creating any dependency on MACH production.
