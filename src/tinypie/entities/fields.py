from abc import ABC, abstractmethod
from typing import Any, Optional

class Field(ABC):
    """
    """
    @abstractmethod
    def validate(self, v: Any) -> bool:
        """
        """
        return False

class StringField(Field):
    """
    """
    def __init__(self,
                 format: Optional[str] = None,
                 max_length: Optional[int] = None,
                 min_length: Optional[int] = None,
                 pattern: Optional[int] = None):
        """
        """
        raise NotImplementedError

    def validate(self, v):
        raise NotImplementedError

class FloatField(Field):
    """
    """
    def __init__(self,
                 maximum: Optional[float] = None,
                 exclusive_maximum: Optional[float] = None,
                 minimum: Optional[float] = None,
                 exclusive_minimum: Optional[float] = None):
        """
        """
        raise NotImplementedError

    def validate(self, v):
        raise NotImplementedError

class IntField(Field):
    """
    """
    def __init__(self,
                 maximum: Optional[float] = None,
                 exclusive_maximum: Optional[float] = None,
                 minimum: Optional[float] = None,
                 exclusive_minimum: Optional[float] = None,
                 multiple_of: Optional[int] = None):
        """
        """
        raise NotImplementedError

    def validate(self, v):
        """
        """
        raise NotImplementedError
