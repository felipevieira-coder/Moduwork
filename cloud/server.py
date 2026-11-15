"""Minimal access-controlled dashboard and heartbeat; no contact-level API."""
from __future__ import annotations

import hmac
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from worker import RuntimeState, worker_loop

DATA_DIR = os.getenv("DATA_DIR", "/data")
STATE = RuntimeState(DATA_DIR)
STOP = threading.Event()
DASHBOARD = Path(__file__).with_name("dashboard.html").read_bytes()


class Handler(BaseHTTPRequestHandler):
    server_version = "ModuCloud/1.0"

    def log_message(self, format, *args):
        # No request headers, tokens, IPs or personal data in cloud logs.
        return

    def send(self, status, content, content_type="application/json; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/healthz":
            self.send(200, b'{"up":true}')
            return
        if route == "/":
            self.send(200, DASHBOARD, "text/html; charset=utf-8")
            return
        if route == "/api/status":
            expected = os.getenv("STATUS_TOKEN", "")
            received = self.headers.get("Authorization", "")
            authorized = bool(expected) and hmac.compare_digest(
                received.encode(), ("Bearer " + expected).encode()
            )
            if not authorized:
                self.send(401, b'{"error":"unauthorized"}')
                return
            self.send(200, json.dumps(STATE.snapshot(), ensure_ascii=False).encode())
            return
        self.send(404, b'{"error":"not_found"}')


def main():
    task = threading.Thread(target=worker_loop, args=(STATE, STOP),
                            name="modu-worker", daemon=True)
    task.start()
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever(poll_interval=0.5)
    finally:
        STOP.set()
        server.server_close()


if __name__ == "__main__":
    main()
