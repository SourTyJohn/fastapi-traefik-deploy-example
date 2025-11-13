from dishka import Provider, Scope, provide

from task_manager.application.common import (
    AsyncTransactionManager,
)
from task_manager.application.gateways import TaskGateway, UserGateway

from task_manager.application.interactors.task_add import (
    TaskCreateInteractor,
    TaskCreateInteractorImpl,
)
from task_manager.application.interactors.user_register import (
    UserRegisterInteractor,
    UserRegisterInteractorImpl,
)


class ApiInteractorsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_register(
        self,
        transaction: AsyncTransactionManager,
        user_gateway: UserGateway,
    ) -> UserRegisterInteractor:
        return UserRegisterInteractorImpl(
            transaction,
            user_gateway,
        )

    @provide
    def task_create(
        self,
        transaction: AsyncTransactionManager,
        task_gateway: TaskGateway,
        user_gateway: UserGateway,
    ) -> TaskCreateInteractor:
        return TaskCreateInteractorImpl(
            transaction,
            task_gateway,
            user_gateway,
        )
