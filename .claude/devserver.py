"""Local dev static server for the IW Content Hub.

Identical to `python3 -m http.server` but sends `Cache-Control: no-store` on
every response so freshly-rendered slides and edited app.js/style.css are always
picked up on reload (the default server lets browsers heuristically cache them,
which makes local review show stale content). Production is served by Cloudflare
Pages and is unaffected by this file.

    python3 .claude/devserver.py 4200
"""
import sys, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4200


class NoCacheHandler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    print(f"IW Content Hub dev server (no-cache) on http://localhost:{PORT}  root={ROOT}")
    ThreadingHTTPServer(("", PORT), NoCacheHandler).serve_forever()
