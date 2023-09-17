# FastAPI Imports
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

# Own Imports
from apps.accounts.manager.jwt.handler import auth_handler


class JWTBearer(HTTPBearer):
    """Responsible for persisting authentication on our API routes."""

    def __init__(self, auto_error: bool = True):
        """
        The method __init__() is a constructor of the class JWTBearer

        :param auto_error: If True, the middleware will raise an error
            if the token is invalid. If
        False, the middleware will return a 401 response, defaults to True
        :type auto_error: bool (optional)
        """
        
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        This method checks if the credentials are valid,
        return the credentials. If not, raise an exception.

        :param request: The request object
        :type request: Request

        :return: The token
        :rtype: str
        """
        
        authorization_credentials = await super(JWTBearer, self).__call__(request)

        if authorization_credentials:
            if authorization_credentials.scheme != "Bearer":
                raise HTTPException(403, {"message": "Invalid authentication scheme."})

            if not self.verify_jwt_token(authorization_credentials.credentials):
                raise HTTPException(403, {"message": "Invalid token or expired token."})

            return authorization_credentials.credentials
        raise HTTPException(403, {"message": "Invalid authorization code."})

    def verify_jwt_token(self, token: str) -> bool:
        """
        This method takes a JWT token as an argument,
        decodes it and returns a boolean value.

        :param token: The token that you want to verify
        :type token: str

        :return: A boolean value.
        :rtype: bool
        """

        payload = auth_handler.decode_jwt(token)
        return True if payload is not None else False


jwt_bearer = JWTBearer()