from __future__ import annotations

import secrets

from app.infrastructure.security.hashing import api_key_prefix, hash_api_key


def generate_api_key(environment: str = "test") -> tuple[str, str, str]:
    token = secrets.token_urlsafe(32)
    raw_key = f"mp_{environment}_{token}"
    return raw_key, api_key_prefix(raw_key), hash_api_key(raw_key)
