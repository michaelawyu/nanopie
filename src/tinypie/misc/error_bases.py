from typing import Any, Optional, Union

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
                 message: Optional[str]):
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
                 message: Optional[str]):
        """
        """
        self.source = source
        self.data = data
        super().__init__(message)

class ModelError(ErrorBase):
    """
    """
    def __init__(self,
                 source: Union['Field', 'ModelMetaKls'],
                 message: Optional[str]):
        """
        """
        self.source = source
        super().__init__(message)
