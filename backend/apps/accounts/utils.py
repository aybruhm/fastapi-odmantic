# FastAPI Imports
from fastapi import Request

# Own Imports
from apps.accounts.manager.jwt.handler import auth_handler


async def get_user_email_from_jwt(req: Request) -> str:
    """Responsible for getting the user email address from the token

    Args:
        req (Request): the request object

    Returns:
        str: the user email
    """

    user_token = req.headers.get("authorization").split(" ")[1]
    decoded_payload = auth_handler.decode_jwt(user_token)
    return decoded_payload["user_email"]
