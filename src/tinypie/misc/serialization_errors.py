from typing import Any, Optional

from .error_bases import SerializationError
from ..entities.fields import Field

class UnrecognizedTypeError(SerializationError):
    """
    """
    def __init__(self,
                 field: Field,
                 value: Any = None,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = ('Field {} with the type {} is not supported in the'
                       'given serialzier.').format(field.name, field.field_type)
        super().__init__(field, value, message)

class NotAnObjectError(SerializationError):
    """
    """
    def __init__(self,
                 input: Any,
                 field: Optional[Field] = None,
                 value: Any = None,
                 message: Optional[str] = None):
        if not message:
            message = 'Input ({}) is not an object.'.format(input)
        super().__init__(field, value, message)
