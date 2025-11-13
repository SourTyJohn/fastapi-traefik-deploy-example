import uuid

from sqlalchemy import Table, Column, String, UUID, DateTime, ForeignKey

from task_manager.adapters.postgres.base import metadata, mapper_registry
from task_manager.presentation.middlewares.bearer_auth import Token


tokens_table = Table(
    "api_tokens",
    metadata,
    Column("uid", UUID, primary_key=True, default=uuid.uuid4),
    Column("owner_uid", UUID, ForeignKey("users.uid")),
    Column("token", String),
    Column("expires_at", DateTime),
)


mapper_registry.map_imperatively(Token, tokens_table)
