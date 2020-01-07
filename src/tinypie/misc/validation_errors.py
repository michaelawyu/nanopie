from typing import Any, List, Optional, Union

from .error_bases import ValidationError

class ModelTypeNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 model: 'ModelMetaKls',
                 value: Any,
                 message: Optional[str] = None):
        if not message:
            message = 'Input is not of the type {}.'.format(model.__name__)
        super().__init__(model, value, message)

class RequiredFieldMissingError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'Field',
                 assigned_name: Optional[str],
                 message: Optional[str] = None):
        if not message:
            message = 'Field {} is required but missing.'.format(
                assigned_name)
        super().__init__(field, None, message)

class FieldTypeNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'Field',
                 assigned_name: Optional[str],
                 value: Any,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} is not of the type {}.'.format(
                value, assigned_name, field.get_value_type().__name__)
        super().__init__(field, assigned_name, value, message)

class ListItemTypeNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'ArrayField',
                 assigned_name: Optional[str],
                 value: Any,
                 message: Optional[str] = None):
        if not message:
            message = ('One or more items from {} in field {} '
                       'is not of the type {}.').format(
                            value, 
                            assigned_name,
                            field.item_field.get_value_type().__name__)
        super().__init__(field, assigned_name, value, message)

class StringMaxLengthExceededError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'StringField',
                 assigned_name: Optional[str],
                 value: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} is too long (max: {}).'.format(
                value, assigned_name, field.max_length)
        super().__init__(field, assigned_name, value, message)

class StringMinLengthBelowError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'StringField',
                 assigned_name: Optional[str],
                 value: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} is too short (min: {}).'.format(
                value, assigned_name, field.min_length)
        super().__init__(field, assigned_name, value, message)

class StringPatternNotMatchedError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'StringField',
                 assigned_name: Optional[str],
                 value: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} in field {} does not match pattern {}.'.format(
                value, assigned_name, field.pattern)
        super().__init__(field, assigned_name, value, message)

class NumberMaxExceededError(ValidationError):
    """
    """
    def __init__(self,
                 field: Union['FloatField', 'IntField'],
                 assigned_name: Optional[str],
                 value: Union[float, int],
                 message: Optional[str] = None):
        if not message:
            message = ('{} in field {} is too large '
                       '(max: {}, exclusive: {}).').format(
                            value,
                            assigned_name,
                            field.maximum,
                            field.exclusive_maximum)
        super().__init__(field, assigned_name, value, message)

class NumberMinBelowError(ValidationError):
    """
    """
    def __init__(self,
                 field: Union['FloatField', 'IntField'],
                 assigned_name: Optional[str],
                 value: Union[float, int],
                 message: Optional[str] = None):
        if not message:
            message = ('{} in field {} is too small '
                       '(max: {}, exclusive: {}).').format(
                            value,
                            assigned_name,
                            field.minimum,
                            field.exclusive_minimum)
        super().__init__(field, value, message)

class ListTooManyItemsError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'ArrayField',
                 assigned_name: Optional[str],
                 value: List[Any],
                 message: Optional[str] = None):
        if not message:
            message = '{} in field {} has too many items (max: {}).'.format(
                value, assigned_name, field.max_items)
        super().__init__(field, assigned_name, value, message)

class ListTooLittleItemsError(ValidationError):
    """
    """
    def __init__(self,
                 field: 'ArrayField',
                 assigned_name: Optional[str],
                 value: List[Any],
                 message: Optional[str] = None):
        if not message:
            message = '{} in field {} has too little items (mix: {}).'.format(
                value, assigned_name, field.min_items)
        super().__init__(field, assigned_name, value, message)

