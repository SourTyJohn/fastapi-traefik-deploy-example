from dishka import Provider, Scope, provide

from task_manager.application.common import (
    AsyncTransactionManager,
)
from task_manager.application.gateways import RealmGateway, UserGateway

from task_manager.application.interactors.realm_add import (
    RealmCreateInteractor,
    RealmCreateInteractorImpl,
)
from task_manager.application.interactors.realm_own_list import (
    RealmOwnListInteractor,
    RealmOwnListInteractorImpl,
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
    def realm_create(
        self,
        transaction: AsyncTransactionManager,
        realm_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> RealmCreateInteractor:
        return RealmCreateInteractorImpl(
            transaction,
            realm_gateway,
            user_gateway,
        )

    @provide
    def realm_own_list(
        self,
        transaction: AsyncTransactionManager,
        realm_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> RealmOwnListInteractor:
        return RealmOwnListInteractorImpl(
            transaction,
            realm_gateway,
            user_gateway,
        )
