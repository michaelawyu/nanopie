from typing import Any, Optional, Union

class ErrorBase(Exception):
    """
    """
    pass

class ValidationError(ErrorBase):
    """
    """
    def __init__(self,
                 source: Union['Field', 'Model'],
                 value: Any,
                 message: Optional[str]):
        """
        """
        self.source = source
        self.value = value
        super().__init__(message)

class SerializationError(ErrorBase):
    """
    """
    def __init__(self, field: 'Field', value: Any, message: Optional[str]):
        self.field = field
        self.value = value
        super().__init__(message)
