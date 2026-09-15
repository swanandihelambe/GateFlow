from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from app.database import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    key_hash = Column(String(64), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True)
    api_key_id = Column(Integer, nullable=False)
    method = Column(String(10), nullable=False)
    path = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)