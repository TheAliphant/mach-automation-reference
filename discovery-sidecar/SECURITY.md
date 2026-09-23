# Security and isolation policy

1. Production access is denied by design.
2. Runtime source may not import outbound HTTP/network client libraries.
3. No `mach.gallery` production hostname may appear in runtime source.
4. No wallet private keys, API keys or production credentials.
5. Capability IDs in the lab catalog must start with `lab.mock.`.
6. Sandbox probes return deterministic local fixtures only.
7. `/v1/execute` always returns HTTP 503 with `production_execution_disabled`.
8. Telemetry is written locally only.
9. Rate limiting protects probe endpoints even in lab mode.
10. CI runs isolation tests on every sidecar change.

Any exception requires a new architecture review. Do not weaken these controls to speed up an experiment.
