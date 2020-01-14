from abc import ABC, abstractmethod
from typing import Any

class Serializer(ABC):
    """
    """
    @abstractmethod
    def serialize(self,
                  data: 'Model',
                  ref: Optional['ModelMetaKls'] = None) -> Any:
        """
        """
        return None
    
    @abstractmethod
    def deserialize(self,
                    data: Any,
                    ref: 'ModelMetaKls') -> 'Model':
        """
        """
        return None

class MediaTypeSerializer(Serializer):
    """
    """
    @abstractmethod
    def serialize(self,
                  data: 'Model',
                  ref: Optional['ModelMetaKls'] = None) -> str:
        """
        """
        return ''
    
    @abstractmethod
    def deserialize(self,
                    data: str,
                    ref: 'ModelMetaKls') -> 'Model':
        """
        """
        return None
    
    @property
    def mime_type(self) -> str:
        return ''
