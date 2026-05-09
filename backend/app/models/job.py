import uuid
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import JSON, UUID, Column, DateTime, Integer, String, func
from sqlalchemy.orm import validates

from app.db.base import Base


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEED = "succeed"
    FAILED = "failed"


class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)
    status = Column(SqlEnum(Status, name="job_status"), default=Status.PENDING, nullable=False)
    retries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @validates("max_retries")
    def validate_max_retry_count(self, key, value):
        if int(value) > 10:
            raise ValueError("`Max retry` must not exceed 10")
        return value
