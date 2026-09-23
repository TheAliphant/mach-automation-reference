#!/usr/bin/env python3
"""MACH Discovery Sidecar.

Deliberately production-disconnected. Uses Python stdlib only and performs no
outbound network calls.
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
import uuid
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "capabilities.snapshot.json"
EVENT_DIR = ROOT / ".runtime"
EVENT_PATH = EVENT_DIR / "events.ndjson"
PORT = int(os.environ.get("SIDECAR_PORT", "8787"))
HOST = os.environ.get("SIDECAR_HOST", "127.0.0.1")
PRODUCTION_CONNECTED = False

_RATE = defaultdict(deque)
_RATE_LOCK = threading.Lock()
RATE_WINDOW_SECONDS = 60
RATE_MAX_PROBES = 20


def load_catalog() -> dict:
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        catalog = json.load(f)
    if catalog.get("production_connected") is not False:
        raise RuntimeError("Catalog must remain production-disconnected")
    for cap in catalog.get("capabilities", []):
        if not str(cap.get("id", "")).startswith("lab.mock."):
            raise RuntimeError("Only lab.mock.* capability IDs are allowed")
    return catalog


def tokenize(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9_]+", (text or "").lower()) if len(t) > 1}


def discover(task: str, client: str = "canonical", limit: int = 5) -> list[dict]:
    wanted = tokenize(task)
    matches = []
    for cap in load_catalog().get("capabilities", []):
        descs = cap.get("descriptions", {})
        description = descs.get(client) or descs.get("canonical", "")
        haystack = tokenize(" ".join([
            cap.get("id", ""),
            cap.get("canonical_name", ""),
            " ".join(cap.get("tags", [])),
            description,
        ]))
        score = len(wanted & haystack)
        if score:
            matches.append({
                "id": cap["id"],
                "name": cap["canonical_name"],
                "description": description,
                "score": score,
                "price_usd": cap.get("price_usd", 0),
                "typical_latency_ms": cap.get("typical_latency_ms"),
                "status": cap.get("status"),
            })
    matches.sort(key=lambda x: (-x["score"], x["id"]))
    return matches[: max(1, min(limit, 20))]


def get_capability(capability_id: str) -> dict | None:
    for cap in load_catalog().get("capabilities", []):
        if cap.get("id") == capability_id:
            return cap
    return None


def quote(capability_id: str) -> dict:
    cap = get_capability(capability_id)
    if not cap:
        return {"found": False, "capability_id": capability_id}
    return {
        "found": True,
        "capability_id": capability_id,
        "mode": "lab_only",
        "production_connected": False,
        "price_usd": cap.get("price_usd", 0),
        "typical_latency_ms": cap.get("typical_latency_ms"),
        "status": cap.get("status"),
    }


def allow_probe(identity: str) -> bool:
    now = time.time()
    with _RATE_LOCK:
        q = _RATE[identity]
        while q and now - q[0] > RATE_WINDOW_SECONDS:
            q.popleft()
        if len(q) >= RATE_MAX_PROBES:
            return False
        q.append(now)
        return True


def probe_payload(capability_id: str, payload: dict) -> dict:
    if not capability_id.startswith("lab.mock."):
        return {"ok": False, "error": "only_lab_mock_capabilities_allowed"}

    cap = get_capability(capability_id)
    if not cap:
        return {"ok": False, "error": "capability_not_found"}

    if capability_id == "lab.mock.json-normalize":
        value = payload.get("value")
        if not isinstance(value, dict):
            return {"ok": False, "error": "value_must_be_object"}
        normalized = {k: value[k] for k in sorted(value)}
        return {"ok": True, "result": {"normalized": normalized}, "mode": "lab_only"}

    if capability_id == "lab.mock.url-classify":
        raw = str(payload.get("url", ""))
        category = "unknown"
        if raw.startswith(("http://", "https://")):
            category = "web"
        elif raw.startswith("git@") or raw.endswith(".git"):
            category = "git"
        return {"ok": True, "result": {"category": category}, "mode": "lab_only"}

    if capability_id == "lab.mock.wallet-format":
        address = str(payload.get("address", ""))
        valid = bool(re.fullmatch(r"0x[a-fA-F0-9]{40}", address))
        return {"ok": True, "result": {"valid_format": valid}, "mode": "lab_only"}

    return {"ok": False, "error": "fixture_not_implemented"}


def record_event(event: dict) -> str:
    EVENT_DIR.mkdir(parents=True, exist_ok=True)
    event_id = str(uuid.uuid4())
    row = {
        "event_id": event_id,
        "timestamp_unix": int(time.time()),
        "production_connected": False,
        **event,
    }
    with EVENT_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
    return event_id


def load_text(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def load_json(name: str) -> dict:
    return json.loads(load_text(name))


class Handler(BaseHTTPRequestHandler):
    server_version = "MACHDiscoveryLab/0.1"

    def log_message(self, fmt, *args):
        return

    def _json(self, status: int, payload: dict):
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _text(self, status: int, body: str, content_type: str = "text/plain; charset=utf-8"):
        raw = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _body_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length > 100_000:
            raise ValueError("payload_too_large")
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path == "/health":
            catalog = load_catalog()
            return self._json(200, {
                "status": "ok",
                "mode": "lab_only",
                "production_connected": False,
                "capabilities": len(catalog.get("capabilities", [])),
            })

        if parsed.path == "/capabilities.json":
            return self._json(200, load_catalog())

        if parsed.path == "/.well-known/agent-card.json":
            return self._json(200, load_json("agent-card.json"))

        if parsed.path == "/openapi.json":
            return self._json(200, load_json("openapi.json"))

        if parsed.path == "/llms.txt":
            return self._text(200, load_text("llms.txt"))

        if parsed.path == "/agents.txt":
            return self._text(200, load_text("agents.txt"))

        if parsed.path == "/v1/discover":
            task = (qs.get("task") or [""])[0]
            client = (qs.get("client") or ["canonical"])[0]
            if not task:
                return self._json(400, {"error": "task_required"})
            results = discover(task, client=client)
            record_event({"stage": "discovery", "client": client, "query_intent": task, "match_count": len(results)})
            return self._json(200, {"mode": "lab_only", "results": results})

        if parsed.path == "/v1/quote":
            capability_id = (qs.get("capability_id") or [""])[0]
            if not capability_id:
                return self._json(400, {"error": "capability_id_required"})
            result = quote(capability_id)
            record_event({"stage": "quote", "capability_id": capability_id, "found": result.get("found", False)})
            return self._json(200, result)

        return self._json(404, {"error": "not_found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            body = self._body_json()
        except Exception as exc:
            return self._json(400, {"error": "invalid_json", "detail": str(exc)})

        if parsed.path == "/v1/discover":
            task = str(body.get("task", ""))
            client = str(body.get("client", "canonical"))
            if not task:
                return self._json(400, {"error": "task_required"})
            results = discover(task, client=client)
            record_event({"stage": "discovery", "client": client, "query_intent": task, "match_count": len(results)})
            return self._json(200, {"mode": "lab_only", "results": results})

        if parsed.path == "/v1/quote":
            capability_id = str(body.get("capability_id", ""))
            if not capability_id:
                return self._json(400, {"error": "capability_id_required"})
            result = quote(capability_id)
            record_event({"stage": "quote", "capability_id": capability_id, "found": result.get("found", False)})
            return self._json(200, result)

        if parsed.path == "/v1/probe":
            identity = self.headers.get("X-Agent-Id") or self.client_address[0]
            if not allow_probe(identity):
                return self._json(429, {"ok": False, "error": "probe_rate_limited"})
            capability_id = str(body.get("capability_id", ""))
            payload = body.get("input", {})
            if not isinstance(payload, dict):
                return self._json(400, {"ok": False, "error": "input_must_be_object"})
            started = time.perf_counter()
            result = probe_payload(capability_id, payload)
            latency_ms = round((time.perf_counter() - started) * 1000, 3)
            record_event({
                "stage": "probe",
                "capability_id": capability_id,
                "success": bool(result.get("ok")),
                "latency_ms": latency_ms,
                "agent_id": identity[:200],
            })
            result["latency_ms"] = latency_ms
            return self._json(200 if result.get("ok") else 400, result)

        if parsed.path == "/v1/report-outcome":
            allowed = {
                "discovery_source", "agent_family", "agent_runtime", "client",
                "user_agent", "capability_id", "query_intent", "stage",
                "outcome", "price_usd", "latency_ms", "error", "repeat_window"
            }
            event = {k: body[k] for k in allowed if k in body}
            event["stage"] = event.get("stage", "feedback")
            event_id = record_event(event)
            return self._json(202, {"accepted": True, "event_id": event_id})

        if parsed.path == "/v1/execute":
            record_event({
                "stage": "execute_blocked",
                "capability_id": body.get("capability_id"),
                "outcome": "production_execution_disabled",
            })
            return self._json(503, {
                "ok": False,
                "error": "production_execution_disabled",
                "production_connected": False,
                "message": "This independent discovery lab cannot execute MACH production services."
            })

        if parsed.path == "/a2a":
            return self._json(501, {
                "error": "a2a_protocol_adapter_not_enabled",
                "message": "Agent Card discovery is scaffolded; protocol conformance must be tested before enabling messaging."
            })

        return self._json(404, {"error": "not_found"})


def main():
    if PRODUCTION_CONNECTED:
        raise RuntimeError("Production connectivity is forbidden in Discovery Sidecar")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"MACH Discovery Lab listening on http://{HOST}:{PORT} (production disconnected)")
    server.serve_forever()


if __name__ == "__main__":
    main()
