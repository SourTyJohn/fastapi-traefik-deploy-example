from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)


def create_pg_engine(db_uri: str, db_echo: int) -> AsyncEngine:
    return create_async_engine(
        url=db_uri,
        echo=db_echo,
    )


def create_pg_session_maker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
