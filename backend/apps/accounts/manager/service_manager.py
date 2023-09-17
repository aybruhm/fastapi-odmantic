# Stdlib Imports
from datetime import datetime, timedelta

# FastAPI Imports
from fastapi import HTTPException, status

# Own Imports
from config.secrets import get_settings
from apps.accounts.manager.utils import generate_otp_code
from apps.accounts.manager.jwt.handler import auth_handler
from apps.accounts.manager.email_manager import EmailManager
from apps.accounts.manager.bcrypt_manager import bcrypt_hasher
from apps.accounts.manager.db_manager import (
    get_user_account_by_email,
    update_user_account,
    create_user_otp_timeout,
    update_user_otp_timeout,
    get_user_otp_timeout,
    update_otp_timeout,
)


# Initialize environment variables
settings = get_settings()


async def login_user_account(email: str, password: str) -> str:
    """Responsible for authenticating an user account

    Args:
        email (str): user account email
        password (str): user account password (raw)

    Raises:
        HTTPException: (404) Account does not exist
        HTTPException: (401) Invalid credentials

    Returns:
        str: the signed jwt token
    """

    account = await get_user_account_by_email(email)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exist",
        )

    if not bcrypt_hasher.check_password(password, account.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    jwt_token = auth_handler.sign_jwt(str(account.id), account.primary_email)
    return jwt_token


async def recover_user_account(email: str) -> bool:
    """Responsible for sending out an otp to account email address.

    Args:
        email (str): the account email address

    Returns:
        bool: confirmation that email was sent
    """

    account = await get_user_account_by_email(email)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exist",
        )

    em = EmailManager(email)
    otp_code = generate_otp_code()

    # Create otp timeout for user account
    await create_user_otp_timeout(otp_code, email)

    # Send account recover email to user
    sent = await em.send(
        subject="[ACCOUNT RECOVERY]: Confirmation of Account Ownership",
        content=f"Hello {account.first_name},\n\nKindly use the OTP code ({otp_code}) to recover your account",
        provider="mailtrap",
    )
    return sent


async def resend_otp_code(email: str) -> bool:
    """Responsible for resending out an otp to the account email address

    Args:
        email (str): the account email address

    Returns:
        bool: confirmation that email was sent
    """

    account = await get_user_account_by_email(email)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exist",
        )

    em = EmailManager(email)
    otp_code = generate_otp_code()

    # Update otp timeout for user account
    await update_user_otp_timeout(otp_code, email)

    # Send account recover email to user
    sent = await em.send(
        subject="[ACCOUNT RECOVERY]: Confirmation of Account Ownership",
        content=f"Hello {account.first_name},\n\nKindly use the OTP code ({otp_code}) to recover your account",
        provider="mailtrap",
    )
    return sent


async def verify_otp_code(email: str, otp_code: str) -> bool:
    """Responsible for verifying the otp code associated with an User account.

    Args:
        otp_code (str): the otp code
        email (str): the user email address

    Returns:
        bool: otp is verified
    """

    ngo_otp_timeout = await get_user_otp_timeout(email)

    otp_expiry_datetime = ngo_otp_timeout.date_modified + timedelta(
        minutes=settings.EMAIL_OTP_TIMEOUT
    )
    current_datetime = datetime.now().time()

    if current_datetime > otp_expiry_datetime.time():
        return False

    if otp_code != ngo_otp_timeout.otp_code:
        return False

    await update_otp_timeout(
        email, **{"otp_verified": True, "date_modified": datetime.utcnow()}
    )
    return True


async def complete_recover_account(email: str, password: str):
    """Responsible for completing recovery account for an User account.

    Args:
        email (str): the user email address
        password (str): the password to update the account with

    Returns:
        str: _description_
    """

    ngo_account = await get_user_account_by_email(email)
    if ngo_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exist",
        )

    # Hash new password and update account
    hashed_password = bcrypt_hasher.hash_password(password)
    await update_user_account(
        email,
        **{"password": hashed_password, "date_modified": datetime.utcnow()},
    )
