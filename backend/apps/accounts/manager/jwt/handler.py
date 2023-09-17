# Stdlib Imports
from typing import Dict, Any
from datetime import datetime, timedelta

# FastAPI Imports
from fastapi import HTTPException

# Own Imports
from config.secrets import get_settings

# Third Party Imports
import jwt


class JWTAuthHandler:
    """
    Responsible for:

    - signing,
    - encoding/decoding of tokens
    """

    def __init__(self):
        """
        This method initializes the class with the secret,
        algorithm, and token lifetime.

        :param secret: The secret key used to sign the JWT
        :type secret: str

        :param algorithm: The algorithm used to sign the token
        :type algorithm: str

        :param token_lifetime: The lifetime of the token in seconds
        :type token_lifetime: int
        """

        self.JWT_SECRET = get_settings().JWT_SECRET_KEY
        self.JWT_ALGORITHM = get_settings().JWT_ALGORITHM
        self.TOKEN_LIFETIME = get_settings().JWT_ACCESS_TOKEN_EXPIRES

    def sign_jwt(self, user_id: str, user_email: str) -> str:
        """
        This method creates a JWT token with a user_email and expiration date,
        signs it with a secret key, and returns a response with the token.

        :param user_id: The user's ID
        :type user_id: str

        :param user_email: The user's email address
        :type user_email: str

        :return: The JWT token.
        """

        payload = {
            "user_id": user_id,
            "user_email": user_email,
            "expires": str(datetime.now() + timedelta(minutes=self.TOKEN_LIFETIME)),
        }
        token = jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        return token

    def decode_jwt(self, token: str) -> Dict[str, Any]:
        """
        This method checks if the token is valid,
        return the decoded token, otherwise return an empty dictionary.

        :param token: The token to decode
        :type token: str

        :return: A dictionary of the decoded token | error message.
        """

        decoded_token = jwt.decode(
            token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM]
        )

        if (
            datetime.strptime(decoded_token["expires"], "%Y-%m-%d %H:%M:%S.%f")
            >= datetime.now()
        ):
            return decoded_token
        raise HTTPException(403, {"message": "Token invalid."})


auth_handler = JWTAuthHandler()
