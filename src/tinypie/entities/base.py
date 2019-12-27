from abc import abstractmethod
from typing import Optional

class Entity:
    """
    """

    @abstractmethod
    def serialize(self) -> str:
        """
        """
        return ""
    
    @abstractmethod
    def deserialize(self) -> Optional[Entity]:
        """
        """
        return None
