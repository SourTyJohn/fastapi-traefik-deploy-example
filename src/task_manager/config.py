import os
from dataclasses import dataclass

from datetime import timedelta

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class Config:
    db: "DbConfig"
    web: "WebConfig"
    auth: "AuthConfig"


@dataclass
class DbConfig:
    DB_URI: str
    DB_ECHO: int


@dataclass
class WebConfig:
    SECRET_KEY: str
    NETWORK_BACKEND_URL: str


@dataclass
class AuthConfig:
    TOKEN_HEADER_NAME: str
    TOKEN_AUTH_SCHEME: str
    TOKEN_EXPIRE_TIMEDELTA: timedelta


def load_env_config() -> Config:
    db_config = DbConfig(
        DB_URI=f"postgresql+psycopg://{os.environ['DB_CONNECTION_STRING']}",
        DB_ECHO=int(os.environ["BACKEND_DB_ECHO"]),
    )

    web_config = WebConfig(
        SECRET_KEY=os.environ["BACKEND_SECRET_KEY"],
        NETWORK_BACKEND_URL=os.environ["NETWORK_BACKEND_URL"],
    )

    auth = AuthConfig(
        TOKEN_HEADER_NAME="Authorization",
        TOKEN_AUTH_SCHEME="Bearer",
        TOKEN_EXPIRE_TIMEDELTA=timedelta(days=1),
    )

    return Config(
        db=db_config,
        web=web_config,
        auth=auth,
    )
