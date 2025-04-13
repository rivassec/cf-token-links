import json
import os
from app import app, parse_duration


def test_parse_duration():
    assert parse_duration("1d").total_seconds() == 86400
    assert parse_duration("2h").total_seconds() == 7200


def test_generate_token_route():
    with app.test_client() as client:
        res = client.post(
            "/api/generate",
            json={"url": "https://example.com", "expires_in": "1h", "max_uses": 1},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert "token" in data
        assert data["link"].startswith("http://localhost")
