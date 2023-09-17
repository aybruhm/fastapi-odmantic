# Stdlib Imports
from datetime import datetime

# Third Party Imports
from pydantic import EmailStr
from odmantic import Field, Model, Reference


class User(Model):
    first_name: str
    last_name: str
    primary_email: EmailStr = Field(index=True)
    email_verified: bool = Field(default=False)
    password: str = Field()
    is_admin: bool = Field(default=False)
    # add more fields
    date_created: datetime
    date_modified: datetime = Field(default=datetime.utcnow())

    class Config:
        collection = "users"


class OTPTimeout(Model):
    user: User = Reference()
    otp_code: str
    otp_verified: bool = Field(default=False)
    date_created: datetime
    date_modified: datetime = Field(default=datetime.utcnow())

    class Config:
        collection = "otp_timeouts"
