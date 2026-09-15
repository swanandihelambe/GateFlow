import time
from threading import Lock


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = Lock()

    def allow_request(self) -> tuple[bool, int]:
        with self.lock:
            now = time.monotonic()
        elapsed = now - self.last_refill

        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )

        self.last_refill = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True, int(self.tokens)

        return False, 0

class RateLimiter:
    def __init__(self, capacity: int = 5, refill_rate: float = 0.5):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = {}
        self.lock = Lock()

    def allow_request(self, client_id: str) -> tuple[bool, int]:
        with self.lock:
            if client_id not in self.buckets:
                self.buckets[client_id] = TokenBucket(
                    self.capacity,
                    self.refill_rate
                )

            bucket = self.buckets[client_id]

        return bucket.allow_request()