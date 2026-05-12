#!/usr/bin/env python3
import argparse
import json
import socket
import subprocess
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


CONFIG = {
    "ping": "1.1.1.1",
    "dns": "github.com",
    "http": "https://github.com",
}


def check_ping(target):
    started = time.perf_counter()
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", target],
        capture_output=True,
        text=True,
        check=False,
    )
    latency = round((time.perf_counter() - started) * 1000, 2)
    return {"name": "ping", "target": target, "ok": result.returncode == 0, "ms": latency}


def check_dns(domain):
    started = time.perf_counter()
    try:
        socket.getaddrinfo(domain, 80)
        ok = True
        error = None
    except OSError as exc:
        ok = False
        error = str(exc)

    return {
        "name": "dns",
        "target": domain,
        "ok": ok,
        "ms": round((time.perf_counter() - started) * 1000, 2),
        "error": error,
    }


def check_http(url):
    started = time.perf_counter()
    try:
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "network-monitor"})
        with urllib.request.urlopen(request, timeout=4) as response:
            status = response.status
        ok = 200 <= status < 400
        error = None
    except Exception as exc:
        status = None
        ok = False
        error = str(exc)

    return {
        "name": "http",
        "target": url,
        "ok": ok,
        "status": status,
        "ms": round((time.perf_counter() - started) * 1000, 2),
        "error": error,
    }


def get_status():
    checks = [
        check_ping(CONFIG["ping"]),
        check_dns(CONFIG["dns"]),
        check_http(CONFIG["http"]),
    ]
    return {"ok": all(item["ok"] for item in checks), "checks": checks, "updated_at": int(time.time())}


def render_page(data):
    cards = []
    for item in data["checks"]:
        state = "ok" if item["ok"] else "falhou"
        extra = item.get("status") or item.get("error") or ""
        cards.append(
            f"""
            <article class="{state}">
              <strong>{item["name"]}</strong>
              <span>{item["target"]}</span>
              <b>{state}</b>
              <small>{item["ms"]}ms {extra}</small>
            </article>
            """
        )

    return f"""<!doctype html>
<html lang="pt-BR">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>network-monitor</title>
<style>
body {{ margin: 0; background: #050607; color: #f8fafc; font-family: monospace; }}
main {{ width: min(760px, calc(100% - 32px)); margin: 40px auto; }}
h1 {{ font-size: 24px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
article {{ border: 1px solid #334155; border-radius: 8px; padding: 14px; background: #0f172a; }}
article.ok b {{ color: #22c55e; }}
article.falhou b {{ color: #ef4444; }}
span, small, b {{ display: block; margin-top: 8px; }}
span, small {{ color: #94a3b8; }}
</style>
<main>
  <h1>network-monitor</h1>
  <p>checks locais simples</p>
  <section class="grid">{''.join(cards)}</section>
</main>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = get_status()
        if self.path == "/api/status":
            body = json.dumps(data, indent=2).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        body = render_page(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description="monitor local simples")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5176)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"network-monitor em http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

