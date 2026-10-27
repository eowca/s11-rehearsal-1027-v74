import http.server
import os
import sys
import time

mode = sys.argv[1] if len(sys.argv) > 1 else "resident"
print("dummy.start", mode, flush=True)
if mode == "cron":
    print("dummy.extractor.loaded", flush=True)
    time.sleep(10)
    print("dummy.completed failed=0", flush=True)
else:
    if mode == "slow-start":
        time.sleep(180)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            body = b"dummy.ready\n"
            self.send_response(200 if self.path == "/ready" else 404)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = http.server.HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler)
    print("dummy.ready", flush=True)
    server.serve_forever()
