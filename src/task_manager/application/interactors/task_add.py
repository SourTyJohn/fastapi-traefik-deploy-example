from typing import Protocol
from dataclasses import dataclass
from abc import abstractmethod

from task_manager.application.common import (
    AsyncTransactionManager,
)
from task_manager.application.gateways import TaskGateway, UserGateway

from task_manager.domain.services.task import TaskService
from task_manager.domain.models import TaskId, UserId


@dataclass
class TaskCreateDTO:
    user_id: UserId
    task_name: str
    task_description: str


class TaskCreateInteractor(Protocol):
    @abstractmethod
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        task_gateway: TaskGateway,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, data: TaskCreateDTO) -> TaskId:
        raise NotImplementedError


class TaskCreateInteractorImpl(TaskCreateInteractor):
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        task_gateway: TaskGateway,
        user_gateway: UserGateway,
    ) -> None:
        self.transaction = transaction
        self.task_gateway = task_gateway
        self.user_gateway = user_gateway

    async def __call__(self, data: TaskCreateDTO) -> TaskId:
        user = await self.user_gateway.get_existing(data.user_id)

        task = TaskService().create(
            owner=user,
            name=data.task_name,
            description=data.task_description,
        )

        task_id = await self.task_gateway.save(task)

        await self.transaction.commit()

        return task_id
