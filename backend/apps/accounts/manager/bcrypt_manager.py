# Third Party Imports
from passlib.context import CryptContext


class BcryptPasswordHasher:
    """
    Responsible for the following:

    - hashing password
    - check/verify hashed password
    """

    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """
        This method takes a password as a string and returns a
        hashed password as a string.

        :param password: The password to hash
        :type password: str

        :return: The hashed password.
        :rtype: str
        """

        return self.ctx.hash(password)

    def check_password(self, password: str, hashed_password: str) -> bool:
        """
        This method checks if the given password matches the hashed_password.

        :param password: The password to be checked
        :type password: str

        :param user: The hashed password that we're checking the password for
        :type hashed_password: str

        :return bool: True if the password matches the hashed password.
        :rtype bool: bool
        """

        return self.ctx.verify(password, hashed_password)


bcrypt_hasher = BcryptPasswordHasher()
