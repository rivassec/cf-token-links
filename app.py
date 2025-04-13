
import json
import os
import secrets
from datetime import datetime, timedelta
from flask import Flask, request, redirect, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

TOKEN_STORE_PATH = "token_store.json"


# Load or initialize the token store
def load_tokens():
    if not os.path.exists(TOKEN_STORE_PATH):
        return {}
    with open(TOKEN_STORE_PATH, "r") as f:
        return json.load(f)


def save_tokens(tokens):
    with open(TOKEN_STORE_PATH, "w") as f:
        json.dump(tokens, f, indent=2)


def parse_duration(duration_str):
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    amount = int(duration_str[:-1])
    unit = duration_str[-1]
    return timedelta(seconds=amount * units[unit])


@app.route("/profile")
@limiter.limit("20 per minute")
def resolve_token():
    token = request.args.get("token")
    if not token:
        abort(400, "Missing token")

    tokens = load_tokens()
    data = tokens.get(token)
    if not data:
        abort(403, "Invalid or expired token")

    now = datetime.utcnow().timestamp()
    if (data.get("expires_at") and now > data["expires_at"]) or (
        data.get("max_uses") is not None and data["uses"] >= data["max_uses"]
    ):
        abort(403, "Token has expired")

    data["uses"] += 1
    tokens[token] = data
    save_tokens(tokens)

    return redirect(data["url"], code=302)


@app.route("/api/generate", methods=["POST"])
@limiter.limit("5 per minute")
def generate_token():
    req = request.get_json()
    target_url = req.get("url")
    expires_in = req.get("expires_in")
    max_uses = req.get("max_uses")
    notes = req.get("notes", "")

    if not target_url or not expires_in:
        abort(400, "Missing required fields")

    token = secrets.token_urlsafe(16)
    now = datetime.utcnow()
    expires_at = (now + parse_duration(expires_in)).timestamp()

    tokens = load_tokens()
    tokens[token] = {
        "url": target_url,
        "created": now.timestamp(),
        "expires_at": expires_at,
        "max_uses": max_uses,
        "uses": 0,
        "notes": notes,
    }
    save_tokens(tokens)

    return jsonify(
        {"token": token, "link": f"http://localhost:5000/profile?token={token}"}
    )


if __name__ == "__main__":
    app.run(debug=True)
