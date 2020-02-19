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

class CredentialError(ErrorBase):
    """
    """
    def __init__(self,
                 message: Optional[str] = None):
        super().__init__(message)

class AuthenticationError(ErrorBase):
    """
    """
    def __init__(self,
                 message: Optional[str] = None):
        super().__init__(message)

class HTTPAuthenticationError(ErrorBase):
    """
    """
    def __init__(self,
                 http_status_code: int,
                 headers: Dict,
                 body_text: str,
                 message: Optional[str] = None):
        """
        """
        self.http_status_code = http_status_code
        self.headers = headers
        self.body_text = body_text
        super().__init__(message)
