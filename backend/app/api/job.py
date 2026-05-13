from typing import Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi_pagination import Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.logging import setup_logger
from app.imagekitio.imagekit import upload_file
from app.models.job import Job
from app.queue.redis_queue import enqueue, remove_job
from app.schemas.job import CustomPagination, JobResponse, Names

logger = setup_logger(__name__)

router = APIRouter()

EXCLUDED_IPS = {settings.ADMIN_IP_ADDRESS}


def get_real_ip(request: Request) -> str | None:
    # Get the X-Forwarded-For header (set by Render)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # The first IP is the client IP (e.g., "client_ip, proxy1, proxy2")
        ip = forwarded_for.split(",")[0].strip()
        return ip
    # Fallback to direct remote address (unlikely to be needed on Render)
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
    logger.info(f"{'-' * 100}")
    logger.info(f"IP Address: {request.headers.get('X-Forwarded-For')}")
    logger.info(f"{'-' * 100}")
    params = Params(page=page, size=size)
    jobs = (
        db.query(Job)
        .filter(Job.created_by == request.client.host)
        .order_by(Job.created_at.desc())
    )
    paginated_data = paginate(jobs, params=params)

    res_data = CustomPagination(
        items=[
            JobResponse.model_validate(i).model_dump() for i in paginated_data.items
        ],
        size=paginated_data.size,
        page=paginated_data.page,
        pages=paginated_data.pages,
        total=paginated_data.total,
        db=db,
    )

    return res_data


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
    logger.info("Create job...")
    logger.info(f"{'-' * 100}")
    logger.info(f"IP Address: {request.headers.get('X-Forwarded-For')}")
    logger.info(f"{'-' * 100}")
    file_dependent_jobs = [Names.IMAGE_OPTIMIZE, Names.MERGE_PDF]

    job = Job(
        name=name,
        max_retries=max_retries,
        created_by=request.client.host,
    )

    if not payload and not files:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, "payload: Field required"
        )

    if payload:
        job.payload = payload

    if name in file_dependent_jobs and files:
        metadata = []
        for file in files:
            if file.size > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_CONTENT,
                    f"File <{file.filename}> exceeded the size limit of {settings.MAX_FILE_SIZE / (1024 * 1024)}MB",
                )

            try:
                uploaded_file = await upload_file(
                    file=file.file,
                    file_name=file.filename,
                )
                data = {
                    "id": uploaded_file.get("id"),
                    "url": uploaded_file.get("url"),
                    "name": uploaded_file.get("name"),
                    "type": uploaded_file.get("type"),
                    "format": file.content_type.split("/")[-1],
                    "size": file.size,
                }
                metadata.append(data)
            except Exception as error:
                logger.error(f"Failed to upload image <{file.filename}> : {error}")
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    f"Something went wrong, please try again later!: {error}",
                )

        job.payload = metadata
    else:
        job.payload = payload

    try:
        db.add(job)
        db.commit()
        db.refresh(job)

        enqueue(job_id=job.id)
    except Exception as error:
        logger.error(f"Failed to create job - Unexpected error: {error}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Unexpected error occurred: {error}",
        )

    return job


@router.delete("/all")
def delete_all(
    db: Session = Depends(get_db),
):
    logger.info("Delete all jobs...")
    jobs = db.query(Job).delete()

    try:
        db.commit()
    except Exception as error:
        logger.error(f"Failed to delete all jobs - Unexpected error: {error}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Something went wrong, please try again later!",
        )
    return {"detail": f"{jobs} jobs deleted successfully"}


@router.delete("/{job_id}")
def delete_job(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    logger.info(f"Delete job <{job_id}>...")
    job = db.query(Job).get(job_id)

    if not job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")

    try:
        # remove job from redis_queue
        remove_job(job_id)
        db.delete(job)
        db.commit()
    except Exception as error:
        logger.error(f"Failed to delete job <{job_id}> - Unexpected error: {error}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Something went wrong, please try again later!",
        )
