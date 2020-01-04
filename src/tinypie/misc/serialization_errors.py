from typing import Any, Optional

from .error_bases import SerializationError

class UnrecognizedTypeError(SerializationError):
    """
    """
    def __init__(self,
                 field: 'Field',
                 value: Any = None,
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = ('Field {} with the type {} is not supported in the'
                       'given serialzier.').format(field.name, field.get_field_type())
        super().__init__(field, value, message)
