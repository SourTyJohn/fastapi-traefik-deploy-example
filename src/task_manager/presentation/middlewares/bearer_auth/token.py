from dataclasses import dataclass
from typing import NewType
from datetime import datetime, timedelta
import secrets


from task_manager.domain.models.id import IdType
from task_manager.domain.models.user import UserId


TokenId = NewType("TokenId", IdType)


@dataclass
class Token:
    uid: TokenId | None
    owner_uid: UserId
    token: str
    expires_at: datetime


class TokenService:
    def _public_token_key(self) -> str:
        return secrets.token_hex(32)

    def generate(self, user_id: UserId, expire_timedelta: timedelta) -> Token:
        return Token(
            uid=None,
            owner_uid=user_id,
            token=self._public_token_key(),
            expires_at=datetime.now() + expire_timedelta,
        )

    def is_expired(self, token: Token) -> bool:
        return token.expires_at < datetime.now()
