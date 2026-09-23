#!/usr/bin/env python3
"""Summarize manually collected Agent Lab result rows."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_rows(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 lab/analyze.py results.ndjson")
    rows = load_rows(sys.argv[1])
    by_framework = defaultdict(Counter)
    for row in rows:
        by_framework[row.get("framework", "unknown")][row.get("outcome", "unknown")] += 1
    print(json.dumps({
        "total": len(rows),
        "by_framework": {k: dict(v) for k, v in sorted(by_framework.items())}
    }, indent=2))


if __name__ == "__main__":
    main()
