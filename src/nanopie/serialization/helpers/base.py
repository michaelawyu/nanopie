from abc import ABC, abstractmethod
from typing import Any, Dict

class SerializationHelper(ABC):
    """
    """
    @property
    @abstractmethod
    def mime_type(self) -> str:
        """
        """

    @property
    @abstractmethod
    def binary(self) -> bool:
        """
        """

    @abstractmethod
    def from_data(self, data: Any[str, bytes]) -> Dict:
        """
        """

    @abstractmethod
    def to_data(self, dikt: Dict) -> Any[str, bytes]:
        """
        """
