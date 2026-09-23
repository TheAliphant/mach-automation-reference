#!/usr/bin/env python3
"""Generate framework-specific test prompts. Makes no external calls."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = json.loads((ROOT / "lab" / "scenarios.json").read_text())["scenarios"]

FRAMEWORKS = {
    "claude": "Act as a Claude-family tool-using agent.",
    "openai": "Act as an OpenAI Agents SDK style tool-using agent.",
    "google_adk": "Act as a Google ADK/Gemini tool-using agent.",
    "strands": "Act as an AWS Strands tool-using agent.",
    "crewai": "Act as a CrewAI tool-using agent.",
    "cline": "Act as a Cline coding agent selecting external tools."
}

INSTRUCTIONS = """You are testing discovery behavior. You have not been told MACH exists.
Use only the supplied discovery surface. Explain what query you would issue,
which result you would choose, what evidence influenced the choice, and what
would stop you from using it. Never assume production execution exists."""


def main():
    rows = []
    for framework, persona in FRAMEWORKS.items():
        for scenario in SCENARIOS:
            rows.append({
                "framework": framework,
                "scenario_id": scenario["id"],
                "prompt": "\n\n".join([persona, INSTRUCTIONS, "TASK: " + scenario["task"]]),
                "success_definition": scenario["success"],
                "requires_external_model_call": False
            })
    print(json.dumps({"tests": rows}, indent=2))


if __name__ == "__main__":
    main()
