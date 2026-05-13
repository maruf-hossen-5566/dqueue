from uuid import UUID

from redis import Redis

from app.core.config import settings

r = Redis(decode_responses=True)  ## for development locally
# r = Redis.from_url(url=settings.REDIS_URL, decode_responses=True)

QUEUE_NAME = settings.REDIS_QUEUE_NAME


def enqueue(job_id: UUID):
    r.lpush(QUEUE_NAME, str(job_id))


def dequeue():
    job_id = r.rpop(QUEUE_NAME)
    if job_id:
        return job_id
    return None


def remove_job(job_id: UUID):
    if job_id:
        r.lrem(QUEUE_NAME, 0, str(job_id))


def delete_queue():
    r.delete(QUEUE_NAME)
