import hashlib
import secrets


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import APIKey


def authenticate_api_key(api_key: str, db: Session) -> APIKey:
    key_hash = hash_api_key(api_key)

    stored_key = (
        db.query(APIKey)
        .filter(
            APIKey.key_hash == key_hash,
            APIKey.is_active == True
        )
        .first()
    )

    if stored_key is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key"
        )

    return stored_key