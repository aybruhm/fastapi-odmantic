# Stdlib Imports
from datetime import datetime

# FastAPI Imports
from fastapi import HTTPException

# Own Imports
from config.database import engine
from apps.accounts.dto.users_dto import UserCreateDTO
from apps.accounts.models.accounts import User, OTPTimeout


async def setup_user_account(payload: UserCreateDTO) -> User:
    """
    Responsible for creating a user account.
    """

    if await user_email_exist(payload.primary_email):
        raise HTTPException(
            status_code=409, detail={"message": "Account already exists"}
        )

    # Initialize user account instance
    user = User(
        **payload.dict(),
        date_created=datetime.utcnow(),
    )

    # Save user to database
    await engine.save(user)
    return user


async def update_user_account(email: str, **kwargs: dict) -> User:
    """
    Responsible for updating user account
    """

    user = await engine.find_one(User, User.primary_email == email)
    user.update(kwargs)

    # Save user to database
    await engine.save(user)
    return user


async def user_email_exist(email: str) -> bool:
    """Checks if user account for the provided email exists.

    Args:
            email (str): the user email address

    Returns:
            bool: account exists
    """

    user = await engine.find_one(User, User.primary_email == email)
    if not user:
        return False
    return True


async def get_user_account_by_email(email: str) -> User:
    """Gets an user account by email.

    Args:
        email (str): the user email address

    Returns:
        User: the user account
    """

    return await engine.find_one(User, User.primary_email == email)


async def create_user_otp_timeout(otp_code: str, email: str):
    """
    Creates an otp timeout for the specified NGO account.

    Args:
        otp_code (str): the otp code
        email (str): the user email address
    """

    user = await get_user_account_by_email(email)

    # Initialize otp_timeout instance and save to database
    otp_timeout = OTPTimeout(
        otp_code=otp_code,
        user=user,
        date_created=datetime.utcnow(),
    )
    await engine.save(otp_timeout)


async def update_user_otp_timeout(otp_code: str, email: str):
    """
    Update the otp code for the specified NGO account.

    Args:
        otp_code (str): the otp code
        email (str): the user email address
    """

    user = await get_user_account_by_email(email)

    # Find account otp timeout document
    otp_timeout = await engine.find_one(OTPTimeout, OTPTimeout.user == user.id)

    # Update otp code and save to database
    otp_timeout.otp_code = otp_code
    otp_timeout.date_modified = datetime.utcnow()
    await engine.save(otp_timeout)


async def update_otp_timeout(email: str, **kwargs: dict):
    """Update otp timeout for the specified NGO account.

    Args:
        email (str): the user email address
    """

    user = await get_user_account_by_email(email)

    # Find account otp timeout document and update it
    otp_timeout = await engine.find_one(OTPTimeout, OTPTimeout.user == user.id)
    otp_timeout.update(kwargs)
    await engine.save(otp_timeout)


async def get_user_otp_timeout(email: str) -> OTPTimeout:
    """
    Retrieve the otp code for a given user account
    """

    user = await get_user_account_by_email(email)
    otp_timeout = await engine.find_one(OTPTimeout, OTPTimeout.user == user.id)
    if not otp_timeout:
        raise HTTPException(400, {"message": "OTP does not exist."})
    return otp_timeout
