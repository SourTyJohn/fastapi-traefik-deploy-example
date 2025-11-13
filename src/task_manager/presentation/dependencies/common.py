from dishka import Provider, Scope, provide

from task_manager.application.common import (
    EncryptionContext,
    EncryptionContextPassword,
)


class CommonsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def encryption_context(self) -> EncryptionContext:
        return EncryptionContextPassword()
