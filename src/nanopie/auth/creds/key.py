from ..base import Credential


class Key(Credential):
    """
    """

    __slots__ = "key"

    def __init__(self, key: str):
        """
        """
        self.key = key
