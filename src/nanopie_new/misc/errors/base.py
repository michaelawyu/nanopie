from abc import ABCMeta
from typing import Any, Optional, Dict, Union

from .mixins import HTTPErrorMixIn

class ErrorBase(Exception, metaclass=ABCMeta):
    """
    """
    def get_message(self, message: Optional[str] = None, **kwargs) -> str:
        """
        """
        if not message:
            if kwargs:
                message = getattr(self, '_message', '') + ' ' + str(kwargs)
            else:
                message = getattr(self, '_message', '')

        return message

class AuthenticationError(ErrorBase, HTTPErrorMixIn, metaclass=ABCMeta):
    """
    """
    def __init__(self,
                 message: Optional[str] = None):
        """
        """
        self.http_status_code = 403
        super().__init__(message=message)

class ErrorWrapper(ErrorBase):
    """
    """
    def __init__(self,
                 wraps: Exception):
        """
        """
        self.wraps = wraps
        super().__init__()

class SerializationError(ErrorBase, HTTPErrorMixIn, metaclass=ABCMeta):
    """
    """
    def __init__(self,
                 source: 'ModelMetaKls',
                 data: Any,
                 message: Optional[str] = None):
        """
        """
        self.source = source
        self.data = data

        self.http_status_code = 400
        super().__init__(message=message)

class ValidationError(ErrorBase, HTTPErrorMixIn, metaclass=ABCMeta):
    """
    """
    def __init__(self,
                 source: Union['Field', 'ModelMetaKls'],
                 data: Any,
                 message: Optional[str] = None):
        """
        """
        self.source = source
        self.data = data

        self.http_status_code = 400
        super().__init__(message=message)
