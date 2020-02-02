from typing import Any, Optional, Dict, Union

class ErrorBase(Exception):
    """
    """
    pass

class ValidationError(ErrorBase):
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
        super().__init__(message)

class SerializationError(ErrorBase):
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
        super().__init__(message)

class AuthenticationError(ErrorBase):
    """
    """
    pass

class HTTPAuthenticationError(ErrorBase):
    """
    """
    def __init__(self,
                 http_status_code: int,
                 headers: Dict,
                 message: Optional[str] = None):
        """
        """
        self.http_status_code = http_status_code
        self.headers = headers
        super().__init__(message)
