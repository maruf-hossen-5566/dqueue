from typing import Callable, Optional
from uuid import UUID

from fastapi import (
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import setup_logger
from app.imagekitio.imagekit import upload_file
from app.models.job import Job
from app.queue.redis_queue import enqueue, remove_job
from app.schemas.job import CustomPagination, JobResponse, Names

logger = setup_logger(__name__)


def __get_jobs(
    request: Request,
    size: int,
    page: int,
    db: Session,
    get_real_ip: Callable,
):
    params = Params(page=page, size=size)
    jobs = (
        db.query(Job)
        .filter(Job.created_by == get_real_ip(request))
        .order_by(Job.created_at.desc())
    )
    paginated_data = paginate(jobs, params=params)

    res_data = CustomPagination(
        ip_address=get_real_ip(request),
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


async def __create_job(
    request: Request,
    name: Names,
    max_retries: int,
    payload: Optional[str],
    files: Optional[list[UploadFile]],
    db: Session,
    get_real_ip: Callable,
):
    file_dependent_jobs = [Names.IMAGE_OPTIMIZE, Names.MERGE_PDF]

    job = Job(
        name=name,
        max_retries=max_retries,
        created_by=get_real_ip(request),
    )

    if not payload and not files:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, "payload: Field required",
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


def __delete_job(
    request: Request,
    job_id: UUID,
    db: Session,
    get_real_ip: Callable,
):
    logger.info(f"Delete job <{job_id}>...")

    user_ip = get_real_ip(request)
    job = (
        db.query(Job)
        .filter(
            Job.created_by == user_ip,
            Job.id == job_id,
        )
        .first()
    )

    if not job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
    elif not str(job.created_by) == user_ip:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You're not authorized")

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

    return {"detail": f"Job <{job_id}> deleted successfully"}
