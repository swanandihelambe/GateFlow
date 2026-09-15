from fastapi import APIRouter, Depends, Header, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import time
import httpx
from app.database import get_db
from app.models import APIKey, RequestLog
from app.security import (
    authenticate_api_key,
    generate_api_key,
    hash_api_key
)
from app.gateway import resolve_route
from app.rate_limiter import RateLimiter

router = APIRouter()

rate_limiter = RateLimiter(
    capacity=5,
    refill_rate=0.5
)

@router.post("/api-keys")
def create_api_key(db: Session = Depends(get_db)):
    api_key = generate_api_key()
    key_hash = hash_api_key(api_key)

    db_api_key = APIKey(key_hash=key_hash)

    db.add(db_api_key)
    db.commit()

#PostgreSQL never receives the plaintext API key.
#And we're deliberately returning the raw key here because this is the creation response. 
#Later, authentication will require the client to send that key back.'''

    return {
        "api_key": api_key
    }

@router.get("/protected")
def protected_endpoint(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    authenticate_api_key(x_api_key, db)

    return {
        "message": "Access granted",
        "service": "GateFlow"
    }


@router.get("/api/{service}")
def proxy_request(
    service: str,
    response: Response,
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    start_time = time.perf_counter()

    api_key = authenticate_api_key(x_api_key, db)

    allowed, remaining = rate_limiter.allow_request(x_api_key)

    response.headers["X-RateLimit-Limit"] = str(rate_limiter.capacity)
    response.headers["X-RateLimit-Remaining"] = str(remaining)

    path = f"/api/{service}"

    if not allowed:
        response.headers["Retry-After"] = "2"

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        log = RequestLog(
            api_key_id=api_key.id,
            method="GET",
            path=path,
            status_code=429,
            response_time_ms=elapsed_ms,
            timestamp=datetime.now(timezone.utc)
        )

        db.add(log)
        db.commit()

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    target_url = resolve_route(path)

    if target_url is None:
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        log = RequestLog(
            api_key_id=api_key.id,
            method="GET",
            path=path,
            status_code=404,
            response_time_ms=elapsed_ms,
            timestamp=datetime.now(timezone.utc)
        )

        db.add(log)
        db.commit()

        raise HTTPException(
            status_code=404,
            detail="Route not found"
        )

    downstream_response = httpx.get(
        target_url,
        timeout=5.0
    )

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    log = RequestLog(
        api_key_id=api_key.id,
        method="GET",
        path=path,
        status_code=downstream_response.status_code,
        response_time_ms=elapsed_ms,
        timestamp=datetime.now(timezone.utc)
    )

    db.add(log)
    db.commit()

    return downstream_response.json()