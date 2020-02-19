from typing import Any, List, Optional, Union

from .base import ValidationError

class ModelTypeNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'ModelMetaKls',
                 data: Any,
                 message: Optional[str] = None):
        if not message:
            message = 'Input is not of the type {}.'.format(source.__name__)
        super().__init__(source=source, data=data, message=message)

class RequiredFieldMissingError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'Field',
                 assigned_name: Optional[str],
                 message: Optional[str] = None):
        if not message:
            message = 'Field {} is required but missing.'.format(
                assigned_name)
        super().__init__(source=source, data=None, message=message)

class FieldTypeNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'Field',
                 assigned_name: Optional[str],
                 data: Any,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} is not of the type {}.'.format(
                data, assigned_name, source.get_data_type().__name__)
        super().__init__(source=source, data=data, message=message)

class ListItemTypeNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'ArrayField',
                 assigned_name: Optional[str],
                 data: Any,
                 message: Optional[str] = None):
        if not message:
            message = ('One or more items from {} in field {} '
                       'is not of the type {}.').format(
                            data, 
                            assigned_name,
                            source.item_field.get_data_type().__name__)
        super().__init__(source=source, data=data, message=message)

class StringMaxLengthExceededError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'StringField',
                 assigned_name: Optional[str],
                 data: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} is too long (max: {}).'.format(
                data, assigned_name, source.max_length)
        super().__init__(source=source, data=data, message=message)

class StringMinLengthBelowError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'StringField',
                 assigned_name: Optional[str],
                 data: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} is too short (min: {}).'.format(
                data, assigned_name, source.min_length)
        super().__init__(source=source, data=data, message=message)

class StringPatternNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'StringField',
                 assigned_name: Optional[str],
                 data: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} does not match pattern {}.'.format(
                data, assigned_name, source.pattern)
        super().__init__(source=source, data=data, message=message)

class NumberMaxExceededError(ValidationError):
    """
    """
    def __init__(self,
                 source: Union['FloatField', 'IntField'],
                 assigned_name: Optional[str],
                 data: Union[float, int],
                 message: Optional[str] = None):
        if not message:
            message = ('{} in field {} is too large '
                       '(max: {}, exclusive: {}).').format(
                            data,
                            assigned_name,
                            source.maximum,
                            source.exclusive_maximum)
        super().__init__(source=source, data=data, message=message)

class NumberMinBelowError(ValidationError):
    """
    """
    def __init__(self,
                 source: Union['FloatField', 'IntField'],
                 assigned_name: Optional[str],
                 data: Union[float, int],
                 message: Optional[str] = None):
        if not message:
            message = ('{} in field {} is too small '
                       '(max: {}, exclusive: {}).').format(
                            data,
                            assigned_name,
                            source.minimum,
                            source.exclusive_minimum)
        super().__init__(source=source, data=data, message=message)

class ListTooManyItemsError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'ArrayField',
                 assigned_name: Optional[str],
                 data: List[Any],
                 message: Optional[str] = None):
        if not message:
            message = '{} in field {} has too many items (max: {}).'.format(
                data, assigned_name, source.max_items)
        super().__init__(source=source, data=data, message=message)

class ListTooLittleItemsError(ValidationError):
    """
    """
    def __init__(self,
                 source: 'ArrayField',
                 assigned_name: Optional[str],
                 data: List[Any],
                 message: Optional[str] = None):
        if not message:
            message = '{} in field {} has too little items (mix: {}).'.format(
                data, assigned_name, source.min_items)
        super().__init__(source=source, data=data, message=message)
