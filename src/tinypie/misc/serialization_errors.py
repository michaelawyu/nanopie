from typing import Any, Optional, Union

from .error_bases import SerializationError

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
            message_tpl = ('Field {} with the type {} is not supported in the'
                       'given serialzier.')
            message = message_tpl.format(source.name, source.get_field_type())
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
