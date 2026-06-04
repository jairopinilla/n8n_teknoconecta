#!/usr/bin/env python3
"""OpenCode Bridge v2 — thin HTTP wrapper using opencode run --continue.
Each POST /ask runs opencode in a subprocess, continuing the last session.
Context is maintained via opencode.db session persistence.
"""

import os
import sys
import json
import time
import subprocess
import signal
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "4097"))
OC_CWD = os.environ.get("OC_CWD", "/srv/opencode-workspace")
TIMEOUT = int(os.environ.get("OC_TIMEOUT", "90"))

def clean_output(text: str) -> str:
    """Remove ANSI codes and noise from opencode output."""
    # ANSI strips
    text = re.sub(r'\x1b\[[?]?\d*[;]?\d*[;]?\d*[a-zA-Z]', '', text)
    text = re.sub(r'\x1b\[[KHJ]', '', text)
    text = re.sub(r'\x1b\[\?25[lh]', '', text)
    text = re.sub(r'\x1b\[\?2026[lh]', '', text)
    
    lines = text.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if 'unknown format' in stripped.lower():
            continue
        if stripped.startswith('> build') or stripped.startswith('> explore'):
            continue
        result.append(stripped)
    
    return '\n'.join(result).strip()

def ask_opencode(message: str, timeout: int = None) -> str:
    """Run opencode with --continue flag to maintain session context."""
    if timeout is None:
        timeout = TIMEOUT
    
    try:
        proc = subprocess.run(
            ["opencode", "run", "--continue", message],
            cwd=OC_CWD,
            capture_output=True,
            timeout=timeout,
            env={**os.environ, "HOME": "/root"},
        )
        
        # Combine stdout and stderr
        output = proc.stdout.decode('utf-8', errors='replace')
        if proc.stderr:
            stderr = proc.stderr.decode('utf-8', errors='replace')
            # Only include stderr if it's not noise
            err_lines = [l for l in stderr.split('\n') 
                       if l.strip() and 'warning' not in l.lower() 
                       and 'unknown format' not in l.lower()]
            if err_lines:
                output += '\n' + '\n'.join(err_lines[:3])
        
        return clean_output(output)
    
    except subprocess.TimeoutExpired:
        return "⏱️ El modelo está tardando demasiado. Intenta de nuevo."
    except Exception as e:
        return f"Error: {str(e)}"

class BridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/ask":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            msg = data.get("message", "")
            to = data.get("timeout", TIMEOUT)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"invalid json"}')
            return

        if not msg:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"empty message"}')
            return

        print(f"[bridge] Q: {msg[:120]}")
        t0 = time.time()
        resp = ask_opencode(msg, to)
        elapsed = time.time() - t0
        print(f"[bridge] A: {resp[:120]} ({elapsed:.1f}s)")

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "response": resp,
            "elapsed": round(elapsed, 1)
        }, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        pass

def main():
    print(f"[bridge] Starting on port {BRIDGE_PORT}, CWD={OC_CWD}")
    
    server = HTTPServer(('0.0.0.0', BRIDGE_PORT), BridgeHandler)
    print(f"[bridge] Listening on :{BRIDGE_PORT}")
    
    def shutdown(sig, frame):
        print("[bridge] Shutdown")
        server.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    server.serve_forever()

if __name__ == "__main__":
    main()
