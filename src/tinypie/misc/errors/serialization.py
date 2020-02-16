from typing import Any, Optional, Union

from .base import SerializationError

class UnrecognizedTypeError(SerializationError):
    """
    """
    def __init__(self,
                 source: 'Field',
                 data: Any = None,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message_tpl = ('Given data ({}) does not match the specified field '
                           '({}) or the field is not supported.')
            message = message_tpl.format(data, source)
        super().__init__(source=source, data=data, message=message)

class NoRefModelError(SerializationError):
    """
    """
    def __init__(self,
                 data: Any,
                 message: Optional[str] = None):
        if not message:
            message_tpl = '{} has no corresponding model for serialization.'
            message = message_tpl.format(data)
        super().__init__(source=None, data=data, message=message)

class NoInputDataError(SerializationError):
    """
    """
    def __init__(self,
                 source: Union['Field', 'ModelMetaKls'],
                 message: Optional[str] = None):
        if not message:
            message = 'No data available for serialization.'
        super().__init__(source=source, data=None, message=message)

class InvalidContentTypeError(SerializationError):
    """
    """
    def __init__(self,
                 expected_content_type: str,
                 incoming_content_type: str,
                 message: Optional[str] = None):
        if not message:
            message = ('Incoming request is of an invalid content type '
                       '({}, expected {}).').format(
                      incoming_content_type, expected_content_type)
        super().__init__(source=None, data=None, message=message)

class RequestTooLargeError(SerializationError):
    """
    """
    def __init__(self,
                 max_content_length: int,
                 incoming_content_length: int,
                 message: Optional[str] = None):
        if not message:
            message = ('Incoming request is too large '
                       '({} bytes, max {} bytes).').format(
                      incoming_content_length, max_content_length)
        super().__init__(source=None, data=None, message=message)
