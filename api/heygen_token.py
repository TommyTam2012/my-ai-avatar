from http.server import BaseHTTPRequestHandler
import os, json, requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # === Load environment keys ===
        admin_key = os.getenv("ADMIN_KEY")
        heygen_key = os.getenv("HEYGEN_API_KEY")

        # === Verify Admin Key from front-end ===
        if self.headers.get("x-admin-key") != admin_key:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return

        # === Call Heygen API to create a fresh streaming token ===
        r = requests.post(
            "https://api.heygen.com/v1/streaming.create_token",
            headers={"Authorization": f"Bearer {heygen_key}"},
            json={"avatar_id": "e30545b4804c4c8fa38487b5be2d6d5c"},
            timeout=10,
        )

        # === Return Heygen’s response to the browser ===
        self.send_response(r.status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(r.content)
