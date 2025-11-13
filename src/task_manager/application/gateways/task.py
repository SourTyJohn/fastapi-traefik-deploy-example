from typing import Protocol
from abc import abstractmethod

from task_manager.application.common.transaction import AsyncTransactionManager
from task_manager.domain.models.task import Task, TaskId


class TaskGateway(Protocol):
    @abstractmethod
    def __init__(self, session: AsyncTransactionManager) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, task: Task) -> TaskId:
        raise NotImplementedError
