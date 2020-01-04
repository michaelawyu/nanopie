from abc import ABC, abstractmethod
import re
from typing import Any, List, Optional

from ..misc.error_bases import FieldValidationError
from ..misc.field_errors import (
    FieldTypeNotMatchedError,
    ListItemTypeNotMatchedError,
    ListTooLittleItemsError,
    ListTooManyItemsError,
    NumberMaxExceededError,
    NumberMinBelowError,
    StringMaxLengthExceededError,
    StringMinLengthBelowError,
    StringPatternNotMatchedError
)

class Field(ABC):
    """
    """
    @abstractmethod
    def get_value_type(self) -> type:
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
                 name: Optional[str] = None,
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
        self.name = name if name else 'Anonymous'
        self.format = format
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
        self.required = required
        self.description = description if description else 'N/A'
        self.resource_identifier = resource_identifier
        if default:
            try:
                self.validate(default)
            except FieldValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return str

    def validate(self, v: Any):
        """
        """
        if type(v) != str:
            raise FieldTypeNotMatchedError(self, v)

        if self.max_length and len(v) > self.max_length:
            raise StringMaxLengthExceededError(self, v)
        
        if self.min_length and len(v) < self.min_length:
            raise StringMinLengthBelowError(self, v)
        
        if not re.match(self.pattern, v):
            raise StringPatternNotMatchedError(self, v)

    def __str__(self):
        """
        """
        print('StringField {}: {}').format(name, description)
        print('This StringField has the following constraints specified:')
        print('\tMax Length: {}'.format(self.max_length))
        print('\tMin Length: {}'.format(self.min_length))
        print('\tPattern: {}'.format(self.pattern))
        print('\tRequired: {}'.format(self.required))
        print('\tResource Identifier: {}'.format(self.resource_identifier))

class FloatField(Field):
    """
    """
    def __init__(self,
                 name: Optional[str] = None,
                 maximum: Optional[float] = None,
                 exclusive_maximum: Optional[bool] = None,
                 minimum: Optional[float] = None,
                 exclusive_minimum: Optional[bool] = None,
                 required: bool = False,
                 default: Optional[float] = None,
                 description: str = ''):
        """
        """
        self.name = name if name else 'Anonymous'
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.required = required
        self.description = description if description else 'N/A'
        if default:
            try:
                self.validate(default)
            except FieldValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return float

    def validate(self, v: Any):
        """
        """
        if type(v) != float:
            raise FieldTypeNotMatchedError(self, v)

        if self.maximum and v >= self.maximum:
            if self.exclusive_maximum and v == self.maximum:
                pass
            else:
                raise NumberMaxExceededError(self, v)
        
        if self.minimum and v <= self.minimum:
            if self.exclusive_minimum and v == self.minimum:
                pass
            else:
                raise NumberMinBelowError(self, v)

class IntField(Field):
    """
    """
    def __init__(self,
                 name: Optional[str] = None,
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
        self.name = name if name else 'Anonymous'
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.multiple_of = multiple_of
        self.required = required
        self.description = description if description else 'N/A'
        if default:
            try:
                self.validate(default)
            except FieldValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return int

    def validate(self, v: Any):
        """
        """
        if type(v) != int:
            raise FieldTypeNotMatchedError(self, v)

        if self.maximum and v >= self.maximum:
            if self.exclusive_maximum and v == self.maximum:
                pass
            else:
                raise NumberMaxExceededError(self, v)
        
        if self.minimum and v <= self.minimum:
            if self.exclusive_minimum and v == self.minimum:
                pass
            else:
                raise NumberMinBelowError(self, v)

class BoolField(Field):
    """
    """
    def __init__(self,
                 name: Optional[str] = None,
                 required: bool = False,
                 default: Optional[bool] = None,
                 description: str = ''):
        """
        """
        self.name = name if name else 'Anonymous'
        self.required = required
        self.description = description if description else 'N/A'
        if default:
            try:
                self.validate(default)
            except FieldValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return bool

    def validate(self, v: Any):
        """
        """
        if type(v) != bool:
            raise FieldTypeNotMatchedError(self, v)


class ArrayField(Field):
    """
    """
    def __init__(self,
                 item_field: Field,
                 name: Optional[str] = None,
                 min_items: Optional[int] = None,
                 max_items: Optional[int] = None,
                 required: bool = False,
                 default: Optional[List[Any]] = None,
                 description: str = ''):
        """
        """
        self.name = name if name else 'Anonymous'
        self.item_field = item_field
        self.min_items = min_items
        self.max_items = max_items
        self.required = required
        self.description = description
        if default:
            try:
                self.validate(default)
            except FieldValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return List

    def validate(self, v: List[Any]):
        """
        """
        if type(v) != list:
            raise FieldTypeNotMatchedError(self, v)

        if self.min_items and len(v) < self.min_items:
            raise ListTooLittleItemsError(self, v)
        
        if self.max_items and len(v) > self.max_items:
            raise ListTooManyItemsError(self, v)

        for item in v:
            if type(item) != self.item_field.get_value_type():
                raise ListItemTypeNotMatchedError(self, v)
            self.item_field.validate(item)
