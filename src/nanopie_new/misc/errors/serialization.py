from typing import Any, Optional, Union

from .base import SerializationError

class UnrecognizedTypeError(SerializationError):
    """
    """
    _message = ('Given data does not match the specified field type, '
                'or the field type is not supported.')

    def __init__(self,
                 source: 'Field',
                 data: Any = None,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source, data=data, message=message)
        super().__init__(source=source, data=data, message=message)

class NoRefModelError(SerializationError):
    """
    """
    _message = ('Given data does not have a model for serialization.')

    def __init__(self,
                 data: Any,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(data=data, message=message)
        super().__init__(source=None, data=data, message=message)

class NoInputDataError(SerializationError):
    """
    """
    _message = ('No available data.')

    def __init__(self,
                 source: Union['Field', 'ModelMetaKls'],
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(source=source, message=message)
        super().__init__(source=source, data=None, message=message)

class InvalidContentTypeError(SerializationError):
    """
    """
    _message = ('Request is of an invalid content type.')

    def __init__(self,
                 expected_content_type: str,
                 incoming_content_type: str,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(expected_content_type=expected_content_type,
                                   incoming_content_type=incoming_content_type,
                                   message=message)
        super().__init__(source=None, data=None, message=message)

class RequestTooLargeError(SerializationError):
    """
    """
    _message = ('Request is too large.')

    def __init__(self,
                 max_content_length: int,
                 content_length: int,
                 message: Optional[str] = None):
        """
        """
        message = self.get_message(max_content_length=max_content_length,
                                   content_length=content_length,
                                   message=message)
        super().__init__(source=None, data=None, message=message)
