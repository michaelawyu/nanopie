from abc import ABC, abstractmethod
from typing import Any, List, Optional

class Field(ABC):
    """
    """
    @property
    @abstractmethod
    def field_type(self) -> type:
        return type(None)

    @abstractmethod
    def validate(self, v: Any):
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
                 pattern: Optional[int] = None,
                 required: bool = False,
                 default: Optional[str] = None,
                 description: str = '',
                 resource_identifier: bool = False):
        """
        """
        self.format = format
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
        self.required = required
        self.default = default
        self.description = description
        self.resource_identifier = resource_identifier

    @property
    def field_type(self) -> type:
        return str

    def validate(self, v):
        raise NotImplementedError

class FloatField(Field):
    """
    """
    def __init__(self,
                 maximum: Optional[float] = None,
                 exclusive_maximum: Optional[float] = None,
                 minimum: Optional[float] = None,
                 exclusive_minimum: Optional[float] = None,
                 required: bool = False,
                 default: Optional[float] = None,
                 description: str = ''):
        """
        """
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.required = required
        self.description = description

    @property
    def field_type(self) -> type:
        return float

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
                 multiple_of: Optional[int] = None,
                 required: bool = False,
                 default: Optional[int] = None,
                 description: str = '',
                 resource_identifier: bool = False):
        """
        """
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.multiple_of = multiple_of
        self.required = required
        self.description = description

    @property
    def field_type(self) -> type:
        return int

    def validate(self, v):
        """
        """
        raise NotImplementedError

class BoolField(Field):
    """
    """
    def __init__(self,
                 required: bool = False,
                 default: Optional[bool] = None,
                 description: str = ''):
        """
        """
        self.required = required
        self.description = description

    @property
    def field_type(self) -> type:
        return bool

    def validate(self, v):
        """
        """
        raise NotImplementedError


class ArrayField(Field):
    """
    """
    def __init__(self,
                 item_type: Field,
                 min_items: Optional[int] = None,
                 max_items: Optional[int] = None,
                 required: bool = False,
                 description: str = ''):
        """
        """
        self.item_type = item_type
        self.min_items = min_items
        self.max_items = max_items
        self.required = required
        self.description = description

    @property
    def field_type(self) -> type:
        return List[self.item_type]

    def validate(self, v):
        """
        """
        raise NotImplementedError
