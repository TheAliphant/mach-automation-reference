# Architecture

## Boundary

```text
MACH PRODUCTION                    MACH DISCOVERY SIDECAR
(unmodified)                       (this directory / separate branch)

services                           static lab capability snapshot
payments                           discovery descriptions
execution                          service-agent shell
wallets                            sandbox probes
QA                                 telemetry schema
                                  agent-behaviour lab
        X  no runtime link  X      distribution experiments
```

There is no network, import, credential, database or deployment dependency between the two systems.

## Sidecar components

### Discovery Edge
Serves local, explicitly lab-only metadata:
- `/capabilities.json`
- `/.well-known/agent-card.json`
- `/llms.txt`
- `/agents.txt`
- `/openapi.json`
- `/v1/discover`
- `/v1/quote`

### Service Agent shell
Can:
- discover capabilities
- explain/quote catalog entries
- run deterministic sandbox probes
- collect outcome feedback
- suggest adjacent mock capabilities

Cannot:
- call MACH production
- initiate payments
- execute real services
- access wallets or secrets

### Agent Lab
Produces framework-specific test prompts. It makes **zero model calls** itself.

### Telemetry
Records local events using a documented schema. No external analytics dependency is required.

## Future integration gate

Any future connection to production requires a separate explicit decision and must use a published public interface. It must never make production depend on this sidecar.

The acceptance test is simple:

> Shut the sidecar down or delete it. MACH production must behave identically.
