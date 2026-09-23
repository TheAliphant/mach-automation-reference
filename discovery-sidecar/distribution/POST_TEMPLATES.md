# Community launch assets

Use research-first language. Never imply the Lab is production.

## Google ADK / Gemini

Title: How does an ADK agent choose a tool when nobody tells it the brand?

We built a production-disconnected discovery lab to test exactly that. The agent gets a task, a small capability surface and no hint that MACH exists. We record the search intent, the candidates it considers, the metadata that changes selection, and the reasons it rejects a tool.

Current experiment: compare task-first vs schema-first descriptions for Google ADK.

The useful result is not whether MACH wins. It is learning what an ADK agent actually uses as a trust and selection signal.

Challenge: give your ADK agent a capability need and do not name any provider. Share the query and selection reason.

## AWS Strands

Title: Testing tool discovery as a reliability problem, not a prompt trick

We are running the same capability-discovery tasks across agent frameworks in an isolated lab. For Strands we are testing whether explicit latency, failure semantics and structured-output guarantees change tool selection.

No production services are connected to the lab, so agents can probe safely.

We would especially like failure cases: what metadata makes a Strands agent reject a candidate before execution?

## CrewAI

Title: What makes a crew delegate to an external capability?

We are testing discovery and delegation behavior across multiple agent runtimes. CrewAI gets the same task as other frameworks, but descriptions are varied around role fit, handoff contract and output structure.

The experiment is intentionally unaided: no provider name in the task.

If you run crews, try the challenge and share which capability your crew chose and why.

## Cline / MCP builders

Title: Can a coding agent discover the right tool without being told its name?

We built a tiny lab-only discovery surface with deterministic fixtures and machine-readable schemas. The current Cline experiment measures whether developer-centric naming, no-side-effect guarantees and exact return contracts affect selection.

Everything is sandboxed; production execution is hard-disabled.

What we want most is a failed discovery trace.

## General MCP community

Title: We are measuring MCP discovery, not installs

Question: when an agent needs a capability it has never seen before, what actually makes it choose one server over another?

We are building a public Agent Lab around that question. Same task, multiple runtimes, no brand hint, structured selection reasons. Production is completely disconnected from the lab.

We plan to publish both wins and failures, including the exact query language agents use.

## x402 / agent commerce

Title: Before payment comes discovery: what makes an agent trust an unknown seller?

A wallet-enabled agent can technically pay an endpoint. That does not explain why it should choose that endpoint.

We are isolating the pre-payment funnel: intent → discovery → inspection → free probe → quote → selection/rejection. The lab cannot make a real payment or execute production work.

We are looking for builders who want to test the same task with different agent frameworks.

## Rule for every post

Do:
- publish a concrete question or experiment;
- include enough methodology to reproduce it;
- ask for traces, failure cases and counterexamples;
- state LAB_ONLY / production-disconnected clearly.

Do not:
- write generic promotional copy;
- cross-post identical text;
- claim adoption before measured external use;
- expose real credentials or production execution through the Lab.
