from http.server import BaseHTTPRequestHandler
import os, json, requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        admin_key = os.getenv("ADMIN_KEY")
        heygen_key = os.getenv("HEYGEN_API_KEY")

        if self.headers.get("x-admin-key") != admin_key:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return

        r = requests.post(
            "https://api.heygen.com/v1/streaming.create_token",
            headers={"Authorization": f"Bearer {heygen_key}"},
            json={"avatar_id": "YOUR_AVATAR_ID"},
            timeout=10,
        )

        self.send_response(r.status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(r.content)
