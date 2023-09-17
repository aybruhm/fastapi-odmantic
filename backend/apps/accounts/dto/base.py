# Own Imports
from apps.accounts.manager.bcrypt_manager import bcrypt_hasher

# Third Party Imports
from pydantic import BaseModel, EmailStr, Field, validator


class UserSetupDTO(BaseModel):
    first_name: str
    last_name: str
    primary_email: EmailStr
    password: str = Field(min_length=6, max_length=28)

    @validator("password")
    def encrypt_password(cls, value: str) -> str:
        return bcrypt_hasher.hash_password(value)
