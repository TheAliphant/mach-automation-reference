# Agent discovery experiment queue

Priority is ordered by information value, not marketing value.

| ID | Experiment | Primary frameworks | Metric |
|---|---|---|---|
| E01 | Task-first vs schema-first description | Google ADK, Claude | correct selection rate |
| E02 | Explicit negative boundary vs none | Strands, OpenAI | false-positive rate |
| E03 | Price before description vs after | AgentKit-style/OpenAI | inspection → probe |
| E04 | Latency metadata present vs absent | Strands, CrewAI | selection rate |
| E05 | Deterministic-output wording | Cline, OpenAI | selection + retry |
| E06 | Natural capability name vs technical name | all | unaided discovery rank |
| E07 | Example input/output present vs absent | Claude, Cline | correct call construction |
| E08 | Free probe offered vs quote-only | all commerce-capable agents | probe → intended purchase |
| E09 | Trust receipt / test history present | all | selection confidence |
| E10 | Failure semantics / retry contract | Strands, CrewAI | successful recovery |

## Kill rule

If a variant produces no measurable improvement after sufficient comparable trials, remove it. Do not keep complexity because it sounds sophisticated.

## Promotion gate

Nothing learned here changes MACH production automatically. A winning discovery pattern can only become a candidate for a separate production publishing decision after:
1. repeated Agent Lab evidence,
2. no reliability regression,
3. no schema drift,
4. explicit review of the public metadata change.
