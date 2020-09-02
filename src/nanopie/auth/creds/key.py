"""This module includes the class for key credentials (e.g. API keys).
"""

from ..base import Credential


class Key(Credential):
    """The class for key credentials (e.g. API keys)."""

    __slots__ = "key"

    def __init__(self, key: str):
        """Initializes a key credential.

        Args:
            key (str): The key.
        """
        self.key = key
