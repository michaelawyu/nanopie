"""This module includes the class for user credentials.
"""

from ..base import Credential


class UserCredential(Credential):
    """The class for user credentials."""

    __slots__ = ("username", "password")

    def __init__(self, username: str, password: str):
        """Initializes a user credential.

        Args:
            username (str): The username.
            password (str): The password.
        """
        self.username = username
        self.password = password
