# FastAPI Imports
from fastapi import Depends, HTTPException

# Own Imports
from config.secrets import get_settings
from apps.accounts.models.accounts import User
from apps.accounts.manager.jwt.bearer import jwt_bearer
from apps.accounts.manager.db_manager import get_user_account_by_email

# Third Party Imports
import jwt


# initialize settings
settings = get_settings()


async def get_current_user(token: str = Depends(jwt_bearer)) -> User:
    """
    This function takes a JWT token, decodes it
    and returns the account that the token belongs to.

    :param token: str = Depends(jwt_bearer)
    :type token: str

    :return: An User account.
    :rtype: User
    """

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        raise HTTPException(403, {"message": "Could not validate token."})

    user = await get_user_account_by_email(payload["user_email"])
    if not user:
        raise HTTPException(404, {"message": "User does not exist!"})
    return user


async def get_active_user(current_user: User = Depends(get_current_user)):
    """
    This function checks if the account is not active,
    raises an exception. Otherwise, return the account.

    :param current_user: User = Depends(get_current_user)
    :type current_user: User

    :return: An active User account.
    :rtype: User
    """

    user = await get_user_account_by_email(current_user.primary_email)
    if not user.email_verified:
        raise HTTPException(400, {"message": "User not activated!"})
    return user


async def get_admin_user(
    active_user: User = Depends(get_active_user),
) -> User:
    """
    This function checks if the account is not an admin,
    raise an exception. Otherwise, return the account.

    :param active_user: User = Depends(get_active_user)
    :type active_user: User

    :return: A user with admin privileges.
    :rtype: User
    """

    if not active_user.is_admin:
        raise HTTPException(401, {"message": "Unauthorized to perform this action!"})
    return active_user
