# The $1 Agent Challenge — lab version

## Builder instruction

Give your agent a task. Do not tell it that MACH exists.

Ask it to:
1. discover an external capability that can solve the task,
2. explain why it selected that capability,
3. identify price, schema, latency and trust signals if available,
4. say what would make it reject the capability,
5. stop before any real payment unless the builder explicitly allows it.

For the current Discovery Lab, all probes are free local fixtures and production execution is disabled.

## Research questions

- What exact words did the agent search for?
- Which discovery surface did it use first?
- Did it inspect more than one provider?
- Which metadata affected selection?
- Did it understand limitations?
- Did it attempt a probe?
- What prevented use?
- Would it reuse the same capability?

## Publication format

Framework:
Task:
Discovery query:
Candidates found:
Selected:
Why:
Rejected:
Probe:
Outcome:
What changed on retry:

The goal is not to make MACH look good. The goal is to learn how agents actually choose.
