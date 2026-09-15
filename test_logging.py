from datetime import datetime

from app.database import SessionLocal
from app.models import RequestLog


db = SessionLocal()

try:
    log = RequestLog(
        api_key_id=1,
        method="GET",
        path="/api/users",
        status_code=200,
        response_time_ms=42.5,
        timestamp=datetime.utcnow()
    )

    db.add(log)
    db.commit()

    print("Request log inserted successfully.")

finally:
    db.close()