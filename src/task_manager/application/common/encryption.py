from abc import abstractmethod
from typing import Protocol

from bcrypt import checkpw, hashpw, gensalt


class EncryptionContext(Protocol):
    @abstractmethod
    def hash(self, data: str):
        raise NotImplementedError

    @abstractmethod
    def verify(self, data: str, hash: str):
        raise NotImplementedError


class EncryptionContextPassword(EncryptionContext):
    def hash(self, data: str):
        salt = gensalt()
        return hashpw(data.encode(), salt)

    def verify(self, data: str, hash: str):
        return checkpw(data.encode(), hash.encode())
