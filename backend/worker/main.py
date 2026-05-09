import time

from app.core.logging import setup_logger
from app.db.session import SessionLocal
from app.models.job import Job, Status
from app.queue.redis_queue import dequeue, enqueue
from app.worker_logic.executor import execute_task

logger = setup_logger(__name__)


def worker():
    db = SessionLocal()
    while True:
        job_id = dequeue()

        if not job_id:
            time.sleep(1)
            continue

        job = db.get(Job, job_id)

        if not job:
            logger.error(f"Job <{job_id}> not found")
            continue

        job.status = Status.RUNNING
        db.commit()

        try:
            result = execute_task(task_name=job.name, task_payload=job.payload)
            job.status = Status.SUCCEED
            job.result = result
        except Exception as e:
            job.retries += 1

            if job.retries >= job.max_retries:
                logger.error(f"Job <{job.id}> failed: {str(e)}")
                job.status = Status.FAILED
                job.error = str(e)
            else:
                logger.warning(f"Retrying job <{job.id}>")
                enqueue(job_id=job.id)
                job.status = Status.PENDING

        db.commit()


if __name__ == "__main__":
    worker()
