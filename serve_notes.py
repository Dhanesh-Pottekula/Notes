"""Serve the Notes folder and save each page's highlights + notes beside it as <page>.notes.json.

Open pages through this server (not file://, not a per-book server) so annotate.js can save to files:
    python3 serve_notes.py            # http://127.0.0.1:8780/  (run from anywhere)
    python3 serve_notes.py 8781

GET  /__notes?page=<path from Notes root, e.g. system_design/ddia/ch06_partitioning.html>  -> the JSON, or null
PUT  /__notes?page=...   body = JSON from annotate.js  -> writes <page minus .html>.notes.json (deletes it when empty)
Everything else is served as static files from this folder. Binds to 127.0.0.1 only.
"""
import json, os, sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8780


def notes_path(query):
    page = (parse_qs(query).get("page") or [""])[0]
    full = os.path.realpath(os.path.join(ROOT, page))
    if not page.endswith(".html") or not full.startswith(ROOT + os.sep) or not os.path.isfile(full):
        return None
    return full[: -len(".html")] + ".notes.json"


class Handler(SimpleHTTPRequestHandler):
    def send_json(self, code, body):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/__notes":
            return super().do_GET()
        target = notes_path(url.query)
        if not target:
            return self.send_json(400, '{"error":"bad page"}')
        if not os.path.exists(target):
            return self.send_json(200, "null")
        with open(target, "rb") as f:
            self.send_json(200, f.read())

    def do_PUT(self):
        url = urlparse(self.path)
        target = notes_path(url.query) if url.path == "/__notes" else None
        if not target:
            return self.send_json(400, '{"error":"bad page"}')
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            items = data["items"]
        except (ValueError, KeyError, TypeError):
            return self.send_json(400, '{"error":"bad body"}')
        if items:
            tmp = target + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
                f.write("\n")
            os.replace(tmp, target)
        elif os.path.exists(target):
            os.remove(target)
        self.send_json(200, '{"ok":true}')

    def end_headers(self):
        if not urlparse(self.path).path.startswith("/__notes"):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        if urlparse(self.path).path == "/__notes" and self.command == "PUT":
            sys.stderr.write("saved %s\n" % parse_qs(urlparse(self.path).query).get("page", ["?"])[0])


if __name__ == "__main__":
    print(f"Notes on http://127.0.0.1:{PORT}/  (saves <page>.notes.json beside each page)")
    ThreadingHTTPServer(("127.0.0.1", PORT), partial(Handler, directory=ROOT)).serve_forever()
