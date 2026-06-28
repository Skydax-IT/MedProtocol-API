from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

PBKDF2_ITERATIONS = 310_000


def hash_api_key(raw_key: str, salt: str | None = None) -> str:
    salt_bytes = base64.urlsafe_b64decode(salt.encode("ascii")) if salt else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", raw_key.encode("utf-8"), salt_bytes, PBKDF2_ITERATIONS)
    salt_text = base64.urlsafe_b64encode(salt_bytes).decode("ascii")
    digest_text = base64.urlsafe_b64encode(digest).decode("ascii")
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt_text}${digest_text}"


def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations_text, salt_text, digest_text = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_text)
        salt_bytes = base64.urlsafe_b64decode(salt_text.encode("ascii"))
        expected = base64.urlsafe_b64decode(digest_text.encode("ascii"))
    except (ValueError, TypeError):
        return False
    actual = hashlib.pbkdf2_hmac("sha256", raw_key.encode("utf-8"), salt_bytes, iterations)
    return hmac.compare_digest(actual, expected)


def api_key_prefix(raw_key: str) -> str:
    return raw_key[:16]
