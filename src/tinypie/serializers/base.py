from abc import ABC, abstractmethod

from ..entities.model import Model

class SerializerAbstract(ABC):
    """
    """

    @abstractmethod
    def serialize(self, entity: Model) -> str:
        """
        """
        return ''
    
    def deserialize(self, data: str) -> Model:
        """
        """
        return None
