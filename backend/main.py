# main.py
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_KEY = os.getenv("ADMIN_KEY")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

@app.post("/heygen/token")
def heygen_token(x_admin_key: str = Header(None)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    r = requests.post(
        "https://api.heygen.com/v1/streaming.create_token",
        headers={"Authorization": f"Bearer {HEYGEN_API_KEY}"},
        json={"avatar_id": "YOUR_AVATAR_ID"},
        timeout=10,
    )
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail=r.text)
    return r.json()
