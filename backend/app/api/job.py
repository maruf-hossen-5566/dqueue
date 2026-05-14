from typing import Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Query,
    Request,
    UploadFile,
)
from fastapi_pagination import add_pagination
from slowapi import Limiter
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.logging import setup_logger
from app.schemas.job import JobResponse, Names
from app.services.job import (
    __create_job,
    __get_jobs,
    __delete_job,
)

logger = setup_logger(__name__)

router = APIRouter()

EXCLUDED_IPS = {settings.ADMIN_IP_ADDRESS}


def get_real_ip(request: Request) -> str | None:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
        return ip
    return request.client.host


limiter = Limiter(key_func=get_real_ip)
add_pagination(router)


@router.get("/")
def get_jobs(
    request: Request,
    size: int = Query(10, le=20),
    page: int = Query(1),
    db: Session = Depends(get_db),
):
    """
    Parameters
    ----------
    request: Request
    size: int
    page: int
    db: Session

    Returns
    -------
    CustomPagination
        items: list[JobResponse]
        size: int
        page: int
        pages: int
        total: int
        pending_item_count: int
        running_item_count: int
        succeed_item_count: int
        failed_item_count: int
    """
    return __get_jobs(
        request,
        size,
        page,
        db,
        get_real_ip,
    )


@router.post("/", response_model=JobResponse)
@limiter.limit("10/day")
async def create_job(
    request: Request,
    name: Names = Form(),
    max_retries: int = Form(ge=1, le=10),
    payload: Optional[str] = Form(None),
    files: Optional[list[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    """
    Parameters
    ----------
    request: Request
    name: Names
    max_retries: int
    payload: str, optional
    files: UploadFile, optional
    db: Session

    Returns
    -------
    JobResponse
        Created job instance
    """
    return await __create_job(
        request,
        name,
        max_retries,
        payload,
        files,
        db,
        get_real_ip,
    )


@router.delete("/{job_id}")
def delete_job(
    request: Request,
    job_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Parameters
    ----------
    request: Request
    job_id: UUID
    db: Session

    Returns
    -------
    dict
        detail: 'success_message'
    """
    return __delete_job(
        request,
        job_id,
        db,
        get_real_ip,
    )
