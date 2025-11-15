from typing import AsyncIterable

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from dishka import Provider, Scope, provide, AnyOf

from task_manager.application.common import AsyncTransactionManager
from task_manager.config import Config

from task_manager.adapters.postgres import (
    create_pg_session_maker,
    create_pg_engine,
)


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    def get_engine(self, config: Config) -> AsyncEngine:
        return create_pg_engine(
            db_uri=config.db.DB_URI,
            db_echo=config.db.DB_ECHO,
        )

    @provide
    def get_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return create_pg_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, AsyncTransactionManager]]:
        async with session_factory() as session:
            yield session
