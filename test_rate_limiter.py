from app.rate_limiter import RateLimiter


limiter = RateLimiter(capacity=5, refill_rate=0.5)

for request_number in range(1, 8):
    allowed, remaining = limiter.allow_request("test-api-key")

    bucket = limiter.buckets["test-api-key"]

    print(
        f"Request {request_number}: "
        f"{'ALLOWED' if allowed else 'BLOCKED'} | "
        f"tokens={bucket.tokens:.3f} | "
        f"remaining={remaining}"
    )