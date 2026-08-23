#!/usr/bin/env python3
"""Tiny localhost sink: the browser POSTs page HTML here so Task 3 can cache
full article HTML to /program/asr/cache/{doi_slug}.html without piping it
through the agent's context. Loopback only, no auth, no external exposure.
"""
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

CACHE = Path(__file__).resolve().parents[1] / "cache"
CACHE.mkdir(parents=True, exist_ok=True)


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        q = parse_qs(urlparse(self.path).query)
        slug = re.sub(r"[^A-Za-z0-9_.-]", "_", (q.get("slug") or ["unknown"])[0])
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n)
        (CACHE / f"{slug}.html").write_bytes(body)
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"saved {slug} {len(body)}".encode())

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
