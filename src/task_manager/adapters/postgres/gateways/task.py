from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.application.gateways import TaskGateway
from task_manager.domain.models.task import Task, TaskId


class TaskGatewayPostgres(TaskGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, task: Task) -> TaskId:
        self.session.add(task)
        await self.session.flush()
        assert task.uid, "Task ID has not been generated on db side"
        return task.uid
