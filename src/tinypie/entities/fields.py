from abc import ABC, abstractmethod
import re
from typing import Any, List, Optional

from ..misc.error_bases import ValidationError
from ..misc.validation_errors import (
    RequiredFieldMissingError,
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
    def validate(self, v: Any, name: str = 'unnamed'):
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
                 description: str = ''):
        """
        """
        self.format = format
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
        self.required = required
        self.description = description
        if default:
            try:
                self.validate(default, None)
            except ValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return str

    def validate(self, v: Any, name: str = 'unnamed'):
        """
        """
        if type(v) != str:
            if not self.required and v == None:
                pass
            else:
                raise FieldTypeNotMatchedError(self, v, name)

        if self.max_length and len(v) > self.max_length:
            raise StringMaxLengthExceededError(self, v)
        
        if self.min_length and len(v) < self.min_length:
            raise StringMinLengthBelowError(self, v)
        
        if self.pattern and not re.match(self.pattern, v):
            raise StringPatternNotMatchedError(self, v)

    def __str__(self):
        """
        """
<<<<<<< HEAD
        print('StringField Description: {}'.format(self.description))
=======
        print('StringField {}: {}').format(self.name, self.description)
>>>>>>> Minor fixes.
        print('This StringField has the following constraints specified:')
        print('\tFormat: {}'.format(self.format))
        print('\tMax Length: {}'.format(self.max_length))
        print('\tMin Length: {}'.format(self.min_length))
        print('\tPattern: {}'.format(self.pattern))
        print('\tRequired: {}'.format(self.required))
        print('\tDefault Value: {}'.format(self.default))

class FloatField(Field):
    """
    """
    def __init__(self,
                 maximum: Optional[float] = None,
                 exclusive_maximum: Optional[bool] = None,
                 minimum: Optional[float] = None,
                 exclusive_minimum: Optional[bool] = None,
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
        if default:
            try:
                self.validate(default)
            except ValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return float

    def validate(self, v: Any, name: str = 'unnamed'):
        """
        """
        if type(v) != float:
            if not self.required and v == None:
                pass
            else:
                raise FieldTypeNotMatchedError(self, v, name)

        if self.maximum and v >= self.maximum:
            if self.exclusive_maximum and v == self.maximum:
                pass
            else:
                raise NumberMaxExceededError(self, v, name)
        
        if self.minimum and v <= self.minimum:
            if self.exclusive_minimum and v == self.minimum:
                pass
            else:
<<<<<<< HEAD
                raise NumberMinBelowError(self, v, name)
    
    def __str__(self):
=======
                raise NumberMinBelowError(self, v)
    
    def __str__(self):
        """
        """
>>>>>>> Minor fixes.
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
                 description: str = ''):
        """
        """
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.multiple_of = multiple_of
        self.required = required
        self.description = description
        if default:
            try:
                self.validate(default)
            except ValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return int

    def validate(self, v: Any, name: str = 'unnamed'):
        """
        """
        if type(v) != int:
            if not self.required and v == None:
                pass
            else:
                raise FieldTypeNotMatchedError(self, v, name)

        if self.maximum and v >= self.maximum:
            if self.exclusive_maximum and v == self.maximum:
                pass
            else:
                raise NumberMaxExceededError(self, v, name)
        
        if self.minimum and v <= self.minimum:
            if self.exclusive_minimum and v == self.minimum:
                pass
            else:
<<<<<<< HEAD
                raise NumberMinBelowError(self, v, name)
    
    def __str__(self):
=======
                raise NumberMinBelowError(self, v)
    
    def __str__(self):
        """
        """
>>>>>>> Minor fixes.
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
        if default:
            try:
                self.validate(default)
            except ValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return bool

    def validate(self, v: Any, name: str = 'unnamed'):
        """
        """
        if type(v) != bool:
<<<<<<< HEAD
            if not self.required and v == None:
                pass
            else:
                raise FieldTypeNotMatchedError(self, v, name)
=======
            raise FieldTypeNotMatchedError(self, v, 'bool')
    
    def __str__(self):
        """
        """
        raise NotImplementedError
>>>>>>> Minor fixes.

    def __str__(self):
        raise NotImplementedError

class ArrayField(Field):
    """
    """
    def __init__(self,
                 item_field: Field,
                 min_items: Optional[int] = None,
                 max_items: Optional[int] = None,
                 required: bool = False,
                 default: Optional[List[Any]] = None,
                 description: str = ''):
        """
        """
        self.item_field = item_field
        self.min_items = min_items
        self.max_items = max_items
        self.required = required
        self.description = description
        if default:
            try:
                self.validate(default)
            except ValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return List

    def validate(self, v: List[Any], name: str = 'unnamed'):
        """
        """
        if type(v) != list:
            if not self.required and v == None:
                pass
            else:
                raise FieldTypeNotMatchedError(self, v, name)

        if self.min_items and len(v) < self.min_items:
            raise ListTooLittleItemsError(self, v, name)
        
        if self.max_items and len(v) > self.max_items:
            raise ListTooManyItemsError(self, v, name)

        for item in v:
<<<<<<< HEAD
            if type(item) != self.item_field.get_value_type():
                raise ListItemTypeNotMatchedError(self, v, name)
            self.item_field.validate(item)
    
    def __str__(self):
        raise NotImplementedError

class ObjectField(Field):
    """
    """
    def __init__(self,
                 model: 'ModelMetaKls',
                 required: bool = False,
                 default: Optional['Model'] = None,
                 description: str = ''):
        """
        """
        self.model = model
        self.required = required
        self.description = description
        if default:
            try:
                self.validate(default)
            except ValidationError as ex:
                print('Cannot set default value {}.'.format(default))
                raise ex
        self.default = default

    @property
    def get_value_type(self) -> type:
        """
        """
        return self.model

    def validate(self, v: 'Model', name: str = 'unnamed'):
        """
        """
        if v.__class__ is not model:
            if not self.required and v == None:
                pass
            else:
                raise FieldTypeNotMatchedError(self, name, v)

        for k in self.model._fields:
            child_field = self.model._fields[k]
            child_field_value = getattr(v, k)
            child_field.validate(child_field_value, k)

    def __str__(self):
        raise NotImplementedError
=======
            if type(item) != self.item_type:
                raise ListItemTypeNotMatchedError(self, v)
            self.item_type.validate(item)
    
    def __str__(self):
        """
        """
        raise NotImplementedError
>>>>>>> Minor fixes.
