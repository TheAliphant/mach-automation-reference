# MACH external communication plan

## Objective

Become easy for both agents and agent builders to discover **without using production as the experimentation surface**.

## Operating rule

Never advertise an experimental capability as live production. Community content can point only to:
1. the Discovery Lab,
2. a documented public production listing that already exists independently, or
3. published research/results.

## Four communication loops

### 1. Agent-native discovery
Publish machine-readable discovery assets from the lab:
- Agent Card
- capability catalog
- OpenAPI
- llms.txt
- agents.txt
- framework-specific descriptions

Measure: discovery requests, query intents, selected capability, probe conversion.

### 2. Builder communities
Create useful experiments rather than promotional posts.

Core format:
"Five agent frameworks got the same task without being told MACH exists. Here is what they discovered and why."

Target communities:
- Google ADK community
- AWS Strands community
- CrewAI community
- Cline/MCP community
- MCP GitHub discussions
- relevant AI-agent and x402 communities

Rule: adapt the post to each community. No cross-post spam.

### 3. Public Agent Lab
Publish reproducible tests:
- task
- framework
- discovery surface
- candidate tools
- selection
- reason
- failure
- repeat result

The research itself is the marketing.

### 4. Builder activation
Offer tiny copy-paste test packs:
- one discovery instruction
- one task
- one expected output
- one feedback format

No production credentials are required.

## 14-day launch sequence

Days 1–2:
- validate lab isolation
- establish baseline discovery tests for all six frameworks
- record first benchmark

Days 3–4:
- optimize descriptions for Google ADK and Strands
- rerun same scenarios
- publish first methodology note

Days 5–6:
- optimize CrewAI and Cline profiles
- publish Agent Challenge instructions

Day 7:
- first weekly "Agent Discovery Report"

Days 8–10:
- test alternative wording, names, examples and negative boundaries
- identify queries where MACH is not discovered

Days 11–12:
- publish a comparison experiment in relevant builder communities
- collect replies as structured research inputs

Days 13–14:
- rank experiments by discovery lift
- keep winners
- kill weak variants
- decide which discovery metadata is mature enough for a separate production publishing decision

## Metrics

North-star:
- unaided agent discovery rate

Supporting:
- result rank
- inspection rate
- probe rate
- correct-selection rate
- false-positive selection rate
- feedback completion
- repeat discovery
- query-to-capability coverage

## Content pillars

1. Agent buying/discovery behavior
2. Tool-description experiments
3. Cross-framework behavior differences
4. Reliability and failure semantics
5. Machine-to-machine commerce experiments

Avoid generic "AI is the future" content.
