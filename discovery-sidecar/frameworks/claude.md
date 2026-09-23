# Claude / Claude Code discovery profile

Goal: learn the phrases and metadata that cause Claude-family agents to select a capability.

Test variables:
- concise "Use when..." description vs task-first description
- explicit negative boundaries
- exact input/output schema
- deterministic/read-only language
- examples before vs after schema
- capability name matching natural user intent

Primary success metric: correct discovery and selection without mentioning MACH in the task.
