from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from fastapi_pagination import Page
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.job import Status, Job


class CustomPagination(Page[Any]):
    pending_item_count: int = 0
    running_item_count: int = 0
    succeed_item_count: int = 0
    failed_item_count: int = 0

    def __init__(self, db: Session = None, **data):
        super().__init__(**data)

        if db:
            self.pending_item_count = db.query(func.count(Job.id)).filter(Job.status == Status.PENDING).scalar()
            self.running_item_count = db.query(func.count(Job.id)).filter(Job.status == Status.RUNNING).scalar()
            self.succeed_item_count = db.query(func.count(Job.id)).filter(Job.status == Status.SUCCEED).scalar()
            self.failed_item_count = db.query(func.count(Job.id)).filter(Job.status == Status.FAILED).scalar()


class Names(str, Enum):
    SEND_EMAIL = "send_email"
    IMAGE_OPTIMIZE = "image_optimize"
    MERGE_PDF = "merge_pdf"
    QR_CODE_GENERATE = "qrcode_generate"
    STRING_PROCESS = "string_process"


class JobBase(BaseModel):
    name: Names
    payload: dict
    max_retries: int = Field(ge=1, le=10)

    class Config:
        from_attributes = True


class JobCreate(JobBase):
    pass


class JobResponse(BaseModel):
    id: UUID
    name: Names
    max_retries: int
    status: str | None
    retries: int
    result: Optional[list | dict]
    error: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
