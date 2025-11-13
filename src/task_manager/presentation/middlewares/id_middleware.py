from abc import abstractmethod
from typing import Protocol

from fastapi import Request

from task_manager.domain.models.user import UserId


class CurrentUserIdProvider(Protocol):
    @abstractmethod
    def __init__(self, request: Request, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self) -> UserId:
        raise NotImplementedError
