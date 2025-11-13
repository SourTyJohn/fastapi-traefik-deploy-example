from abc import abstractmethod
from typing import Protocol

from passlib.context import CryptContext


class EncryptionContext(Protocol):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def hash(self, data: str):
        raise NotImplementedError

    @abstractmethod
    def verify(self, hash: str, data: str):
        raise NotImplementedError


class EncryptionContextPassword(EncryptionContext):
    def __init__(self) -> None:
        self.context = CryptContext(
            schemes=["argon2", "bcrypt"],
            deprecated="auto",
        )

    def hash(self, data: str):
        return self.context.hash(data)

    def verify(self, hash: str, data: str):
        return self.context.verify(data, hash)
