# Stdlib Imports
from datetime import datetime
from typing import Text, Optional, List

# Own Imports
from apps.accounts.dto.base import UserSetupDTO, validator

# FastAPI Imports
from fastapi import HTTPException

# Third Party Imports
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class UserCreateDTO(UserSetupDTO):
    pass # add extra fields


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str


class UserAccountRecoverDTO(BaseModel):
    email: EmailStr


class UserAccountRecoverConfirmDTO(BaseModel):
    otp_code: str
    email: EmailStr


class UserAccountChangePasswordDTO(BaseModel):
    password: str = Field(min_length=6, max_length=28)
    confirm_password: str = Field(min_length=6, max_length=28)


class UserAccountRecoverCompleteDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=28)
