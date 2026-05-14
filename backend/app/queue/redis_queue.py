from uuid import UUID

from redis import Redis

from app.core.config import settings

# r = Redis(decode_responses=True)  ## locally
r = Redis.from_url(url=settings.REDIS_URL, decode_responses=True)

QUEUE_NAME = settings.REDIS_QUEUE_NAME


def enqueue(job_id: UUID):
    """Enqueue a job ID to the Redis list queue."""
    r.lpush(QUEUE_NAME, str(job_id))


def dequeue():
    """Dequeue and return the rightmost job ID from the Redis list queue."""
    job_id = r.rpop(QUEUE_NAME)
    if job_id:
        return job_id
    return None


def remove_job(job_id: UUID):
    """Remove all occurrences of a job ID from the Redis list queue."""
    if job_id:
        r.lrem(QUEUE_NAME, 0, str(job_id))


def delete_queue():
    """Delete the entire Redis list queue."""
    r.delete(QUEUE_NAME)
