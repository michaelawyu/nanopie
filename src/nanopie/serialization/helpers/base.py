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
        pass

    @property
    @abstractmethod
    def binary(self) -> bool:
        """
        """
        pass

    @abstractmethod
    def from_data(self, data: Any[str, bytes]) -> Dict:
        """
        """
        pass

    @abstractmethod
    def to_data(self, dikt: Dict) -> Any[str, bytes]:
        """
        """
        pass
