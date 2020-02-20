from typing import Any, List, Optional, Union

from .base import ValidationError

class ModelTypeNotMatchedError(ValidationError):
    """
    """
    _message = ('Input is not of the given type.')

    def __init__(self,
                 source: 'ModelMetaKls',
                 data: Any,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source, data=data, message=message)
        super().__init__(source=source, data=data, message=message)

class RequiredFieldMissingError(ValidationError):
    """
    """
    _message = ('A required field is missing.')

    def __init__(self,
                 source: 'Field',
                 assigned_field_name: Optional[str],
                 message: Optional[str] = None):
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   message=message)
        super().__init__(source=source, data=None, message=message)

class FieldTypeNotMatchedError(ValidationError):
    """
    """
    _message = ('Input is not of the given field type.')

    def __init__(self,
                 source: 'Field',
                 assigned_field_name: Optional[str],
                 data: Any,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class ListItemTypeNotMatchedError(ValidationError):
    """
    """
    _message = ('One or more items in the list is not of the given field type.')

    def __init__(self,
                 source: 'ArrayField',
                 assigned_field_name: Optional[str],
                 data: Any,
                 message: Optional[str] = None):
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class StringMaxLengthExceededError(ValidationError):
    """
    """
    _message = ('Input string is too long.')

    def __init__(self,
                 source: 'StringField',
                 assigned_field_name: Optional[str],
                 data: str,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class StringMinLengthBelowError(ValidationError):
    """
    """
    _message = ('Input string is too short.')

    def __init__(self,
                 source: 'StringField',
                 assigned_field_name: Optional[str],
                 data: str,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class StringPatternNotMatchedError(ValidationError):
    """
    """
    _message = ('Input string does not match the given pattern.')

    def __init__(self,
                 source: 'StringField',
                 assigned_field_name: Optional[str],
                 data: str,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class NumberMaxExceededError(ValidationError):
    """
    """
    _message = ('Input number is too large.')

    def __init__(self,
                 source: Union['FloatField', 'IntField'],
                 assigned_field_name: Optional[str],
                 data: Union[float, int],
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class NumberMinBelowError(ValidationError):
    """
    """
    _message = ('Input number is too small.')

    def __init__(self,
                 source: Union['FloatField', 'IntField'],
                 assigned_field_name: Optional[str],
                 data: Union[float, int],
                 message: Optional[str] = None):
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class ListTooManyItemsError(ValidationError):
    """
    """
    _message = ('Input list has too many items.')

    def __init__(self,
                 source: 'ArrayField',
                 assigned_field_name: Optional[str],
                 data: List[Any],
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)

class ListTooLittleItemsError(ValidationError):
    """
    """
    _message = ('Input list has too little items.')

    def __init__(self,
                 source: 'ArrayField',
                 assigned_field_name: Optional[str],
                 data: List[Any],
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source,
                                   assigned_field_name=assigned_field_name,
                                   data=data,
                                   message=message)
        super().__init__(source=source, data=data, message=message)
