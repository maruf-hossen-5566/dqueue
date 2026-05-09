import asyncio

from app.core.logging import setup_logger
from app.tasks.registry import get_registered_task
from app.worker_logic.exception import TaskException

logger = setup_logger(__name__)


def execute_task(task_name: str, task_payload: dict):
    if not task_name.strip():
        raise TaskException("Missing `task_name` in payload")

    task_fun = get_registered_task(task_name)

    if not task_fun:
        raise TaskException(f"Unknown task: {task_name}")

    try:
        return asyncio.run(task_fun(task_payload))
    except Exception as e:
        logger.error(f"Failed to execute task <{task_name}>: {e}")
        raise TaskException(e) from e
