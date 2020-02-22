from typing import Any, Optional, Union

class ServiceError(Exception):
    """
    """
    def __init__(self, *args, response: Optional['RPCResponse'] = None):
        """
        """
        self.response = response
        super().__init__(*args)

class AuthenticationError(ServiceError):
    """
    """

class SerializationError(ServiceError):
    """
    """

class ValidationError(ServiceError):
    """
    """
    def __init__(self,
                 *args,
                 source: Union['Field', 'ModelMetaKls'],
                 data: Any,
                 response: Optional['RPCResponse'] = None):
        """
        """
        self.source = source
        self.data = data

        super().__init__(*args, response=response)

class FoundationError(ServiceError):
    """
    """
