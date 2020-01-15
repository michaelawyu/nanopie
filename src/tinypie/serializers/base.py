from abc import ABC, abstractmethod
from typing import Any, Optional

class Serializer(ABC):
    """
    """
    @abstractmethod
    def serialize(self,
                  data: 'Model',
                  ref: Optional['ModelMetaKls'] = None) -> str:
        """
        """
        return None
    
    @abstractmethod
    def deserialize(self,
                    data: str,
                    ref: 'ModelMetaKls') -> 'Model':
        """
        """
        return None

    @property
    def mime_type(self):
        """
        """
        return ''
