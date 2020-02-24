from ..base import Credential


class UserCredential(Credential):
    """
    """

    __slots__ = ("username", "password")

    def __init__(self, username: str, password: str):
        """
        """
        self.username = username
        self.password = password
