# cf-token-links

[![Checkov Security Scan](https://github.com/rivassec/cf-token-links/actions/workflows/checkov.yml/badge.svg)](https://github.com/rivassec/cf-token-links/actions/workflows/checkov.yml)
[![Trivy Scan](https://github.com/rivassec/cf-token-links/actions/workflows/trivy.yml/badge.svg)](https://github.com/rivassec/cf-token-links/actions/workflows/trivy.yml)
[![Tests](https://github.com/rivassec/cf-token-links/actions/workflows/test.yaml/badge.svg)](https://github.com/rivassec/cf-token-links/actions/workflows/test.yaml)
[![Status](https://img.shields.io/badge/status-work--in--progress-yellow.svg)](#)

> ⚠️ **This project is a work in progress. Interfaces, functionality, and security guarantees may change. Not yet production-ready.**

---

A lightweight Flask-based microservice for generating expiring, token-based redirect links. Useful for sharing time-limited access to profiles or resources (e.g., GitHub, LinkedIn) in a secure and auditable way.

## Features

- Secure token generation using `secrets.token_urlsafe`
- Expiration based on time and usage count
- HTTP 302 redirect for valid tokens
- Token usage tracking and JSON persistence
- Flask-Limiter support for basic rate limiting

## API Overview

### `POST /api/generate`

Generates a new token.

**Request JSON:**

```json
{
  "url": "https://example.com",
  "expires_in": "1d",
  "max_uses": 3,
  "notes": "Optional metadata"
}
```

- `expires_in`: duration string (`30s`, `10m`, `2h`, `1d`)
- `max_uses`: optional integer
- `notes`: optional text (not exposed publicly)

**Response:**

```json
{
  "token": "abc123xyz",
  "link": "http://localhost:5000/profile?token=abc123xyz"
}
```

---

### `GET /profile?token=...`

Redirects to the target URL if the token is valid, not expired, and under the usage limit. Otherwise returns `403 Forbidden`.

---

## Getting Started

### Requirements

- Python 3.12+
- `pip`, `venv` recommended
- Docker (optional, for containerization)

### Install Locally

```bash
git clone https://github.com/yourusername/cf-token-links.git
cd cf-token-links
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## Running with Docker

```bash
docker build -t cf-token-links .
docker run -p 5000:5000 cf-token-links
```

---

## Development and Testing

```bash
pip install pytest
pytest
```

---

## Security Considerations

- Tokens are generated with strong entropy (128-bit+)
- Rate limits are enforced using Flask-Limiter
- Expired or reused tokens return a 403 error
- JSON-based token store is suitable for single-instance use
- For production deployments, consider:
  - Redis backend for rate limiting
  - File locking or SQLite for concurrent-safe persistence
  - HTTPS behind a proxy like Nginx

---

## License

MIT License. See `LICENSE` file for details.
