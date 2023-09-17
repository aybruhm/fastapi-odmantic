# Stdlib Imports
from typing import Dict, Union
from functools import lru_cache

# Pydantic Imports
from pydantic import BaseSettings

# Third-party Imports
from decouple import config as environ


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
    ALLOWED_METHODS: str = environ("ALLOWED_METHODS", cast=str)
    ALLOWED_HEADERS: list = ["*"]
    ALLOWED_ORIGINS: str = environ("ALLOWED_ORIGINS", cast=str)

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
    
    # Cloudinary configuration
    CLOUDINARY_NAME: str = environ("CLOUDINARY_NAME", cast=str)
    CLOUDINARY_API_KEY: str = environ("CLOUDINARY_API_KEY", cast=str)
    CLOUDINARY_API_SECRET: str = environ("CLOUDINARY_API_SECRET", cast=str)



@lru_cache(maxsize=None)
def get_settings() -> Settings:
    """Cache the settings values."""

    return Settings()
