from uuid import UUID

from redis import Redis

from app.core.config import settings

r = Redis(host="localhost", port=6379, decode_responses=True)

QUEUE_NAME = settings.QUEUE_NAME


def enqueue(job_id: UUID):
    r.lpush(QUEUE_NAME, str(job_id))


def dequeue():
    job_id = r.rpop(QUEUE_NAME)
    if job_id:
        return job_id
    return None


def delete_queue():
    r.delete(QUEUE_NAME)
