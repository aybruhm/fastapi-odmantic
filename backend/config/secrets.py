# Stdlib Imports
from functools import lru_cache
from typing import Dict, Union

# Pydantic Imports
from pydantic import BaseSettings

# Third-party Imports
from decouple import RepositoryEnv, config as environ


# Extend supported .env files
environ.SUPPORTED.update({".env.dev": RepositoryEnv})
environ.SUPPORTED.update({".env.prod": RepositoryEnv})


class Settings(BaseSettings):
    """
    Settings for configuring project backend service.
    """

    # main configuration
    API_TITLE: str = "Project Backend Service"
    API_DESCRIPTION: str = ""
    API_VERSION: str = "1.0"
    API_CONTACT: Dict[str, Union[int, str]] = {"email": "me@abram.tech"}

    # cors configuration
    ALLOWED_CREDENTIALS: bool = True
    ALLOWED_METHODS: list = environ("ALLOWED_METHODS").split(",")
    ALLOWED_HEADERS: list = ["*"]
    ALLOWED_ORIGINS: str = environ("ALLOWED_ORIGINS")

    # JWT configuration
    JWT_SECRET_KEY: str = environ("JWT_SECRET_KEY", cast=str)
    JWT_ALGORITHM: str = environ("JWT_ALGORITHM", cast=str)
    JWT_ACCESS_TOKEN_EXPIRES: int = environ(
        "JWT_ACCESS_TOKEN_EXPIRES", cast=int
    )

    # database configuration
    USE_TEST_DB: bool = False
    
    # Email configuration
    EMAIL_MODE: str = environ("EMAIL_MODE", cast=str)
    EMAIL_API_URL: str = environ("EMAIL_API_URL", cast=str)
    EMAIL_HOST_TOKEN: str = environ("EMAIL_HOST_TOKEN", cast=str)
    EMAIL_OTP_TIMEOUT: int = environ("EMAIL_OTP_TIMEOUT", cast=int)
    EMAIL_HOST_SENDER: str = environ("EMAIL_HOST_SENDER", cast=str)


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    """Cache the settings values."""

    return Settings()
