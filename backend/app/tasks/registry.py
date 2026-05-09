from typing import Callable

TASK_REGISTRY = {}


def task(name: str):
    def decorator(func: Callable):
        TASK_REGISTRY[name] = func
        return func

    return decorator


def get_registered_task(name: str):
    return TASK_REGISTRY.get(name)
