from typing import Optional

from .base import CredentialError

class InvalidJWTError(CredentialError):
    """
    """
    def __init__(self,
                 wrapped: 'Exception',
                 message: Optional[str] = None):
        self.wrapped = wrapped
        if not message:
            message = 'The provided JWT is invalid ({}).'.format(
                wrapped.__class__.__name__)
        super().__init__(message)
