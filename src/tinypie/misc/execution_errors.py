from typing import Optional

from .error_bases import ExceptionError

class NoContextPresentError(ExceptionError):
    """
    """
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Working outside of request context.'
        super().__init__(message)
