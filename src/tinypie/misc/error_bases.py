from typing import Any, Optional

from ..entities.fields import Field

class ErrorBase(Exception):
    """
    """
    pass

class FieldValidationError(ErrorBase):
    """
    """
    def __init__(self, field: Field, value: Any, message: Optional[str]):
        self.field = field
        self.value = value
        super().__init__(message)
