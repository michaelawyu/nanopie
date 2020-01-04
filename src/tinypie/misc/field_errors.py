from typing import Any, List, Optional, Union

from .error_bases import ErrorBase, FieldValidationError

class RequiredFieldMissingError(ErrorBase):
    """
    """
    def __init__(self,
                 field: 'Field',
                 field_assigned_name: str,
                 message: Optional[str]):
        self.field = field
        if not message:
            message = 'Field {} ({}) is required but missing.'.format(
                field_assigned_name, field.name)
        super().__init__(message)

class FieldTypeNotMatchedError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: 'Field',
                 value: Any,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} is not of the type {}.'.format(
                value, field.get_value_type().__name__)
        super().__init__(field, value, message)

class ListItemTypeNotMatchedError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: 'ArrayField',
                 value: Any,
                 message: Optional[str] = None):
        if not message:
            message = 'One or more items in {} is not of the type {}.'.format(
                value, field.item_field.get_value_type())
        super().__init__(field, value, message)

class StringMaxLengthExceededError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: 'StringField',
                 value: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} is too long (max length: {}).'.format(
                value, field.max_length)
        super().__init__(field, value, message)

class StringMinLengthBelowError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: 'StringField',
                 value: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} is too short (min length: {}).'.format(
                value, field.min_length)
        super().__init__(field, value, message)

class StringPatternNotMatchedError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: 'StringField',
                 value: str,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = '{} does not match pattern {}.'.format(
                value, field.pattern)
        super().__init__(field, value, message)

class NumberMaxExceededError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: Union['FloatField', 'IntField'],
                 value: Union[float, int],
                 message: Optional[str] = None):
        if not message:
            message = '{} is too large (max: {}, exclusive: {}).'.format(
                value, field.maximum, field.exclusive_maximum)
        super().__init__(field, value, message)

class NumberMinBelowError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: Union['FloatField', 'IntField'],
                 value: Union[float, int],
                 message: Optional[str] = None):
        if not message:
            message = '{} is too small (max: {}, exclusive: {}).'.format(
                value, field.minimum, field.exclusive_minimum)
        super().__init__(field, value, message)

class ListTooManyItemsError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: 'ArrayField',
                 value: List[Any],
                 message: Optional[str] = None):
        if not message:
            message = '{} has too many items (max: {}).'.format(
                value, field.max_items)
        super().__init__(field, value, message)

class ListTooLittleItemsError(FieldValidationError):
    """
    """
    def __init__(self,
                 field: 'ArrayField',
                 value: List[Any],
                 message: Optional[str] = None):
        if not message:
            message = '{} has too little items (mix: {}).'.format(
                value, field.min_items)
        super().__init__(field, value, message)
