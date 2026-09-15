from fastapi import HTTPException

from app.database import SessionLocal
from app.security import authenticate_api_key


db = SessionLocal()

try:
    authenticate_api_key("definitely-invalid-key", db)
except HTTPException as e:
    print(e.status_code, e.detail)
finally:
    db.close()