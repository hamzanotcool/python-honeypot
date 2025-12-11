from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import os

from logger import log_event

# Charger config.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.json")

DEFAULT_CONFIG = {
    "port": 8080,
    "fake_endpoints": ["/", "/login", "/admin", "/api"]
}

try:
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
except Exception:
    CONFIG = DEFAULT_CONFIG

PORT = CONFIG["port"]
FAKE_ENDPOINTS = CONFIG["fake_endpoints"]

FAKE_LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
<h2>Secure Login</h2>
<form method="POST">
    Username: <input name="user"><br><br>
    Password: <input name="pass" type="password"><br><br>
    <input type="submit" value="Login">
</form>
</body>
</html>
"""


class HoneyPotHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path not in FAKE_ENDPOINTS:
            self.send_error(404)
            return

        log_event({
            "event": "HTTP_GET",
            "ip": self.client_address[0],
            "endpoint": self.path,
            "user_agent": self.headers.get("User-Agent")
        })

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(FAKE_LOGIN_PAGE.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(length).decode()
        fields = parse_qs(post_data)

        username = fields.get("user", [""])[0]
        password = fields.get("pass", [""])[0]

        log_event({
            "event": "HTTP_POST",
            "ip": self.client_address[0],
            "endpoint": self.path,
            "username": username,
            "password": password,
            "user_agent": self.headers.get("User-Agent")
        })

        self.send_response(403)
        self.end_headers()
        self.wfile.write(b"Access Denied. All activity is logged.")


def run_server():
    server = HTTPServer(("", PORT), HoneyPotHandler)
    print(f"[+] Honeypot HTTP actif sur le port {PORT}")
    print("[+] CTRL+C pour arrêter.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Honeypot HTTP arrêté.")


if __name__ == "__main__":
    run_server()
