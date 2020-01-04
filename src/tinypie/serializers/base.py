from abc import ABC, abstractmethod

from ..entities.model import Model

class SerializerAbstract(ABC):
    """
    """

    @abstractmethod
    def serialize(self, entity: Model, skip_validation: bool = False) -> str:
        """
        """
        return ''
    
    @abstractmethod
    def deserialize(self,
                    kls: type,
                    data_str: str,
                    skip_validation: bool = True) -> Model:
        """
        """
        return None
