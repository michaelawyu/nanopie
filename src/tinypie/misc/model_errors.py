from typing import Optional

from .error_bases import ModelError

class ResourceParentKlsAlreadyExistsError(ModelError):
    """
    """
    def __init__(self,
                 source: 'Resource',
                 messsage: Optional[str] = None):
        """
        """
        raise NotImplementedError

class ResourceIdentifierFieldAlreadyExistsError(ModelError):
    """
    """
    def __init__(self,
                 source: 'Resource',
                 identifier_field_name: str,
                 message: Optional[str] = None):
        """
        """
        raise NotImplementedError

class ResourceIdentifierFieldNotExists(ModelError):
    """
    """
    def __init__(self,
                 source: 'Resource',
                 identifier_field_name: str,
                 message: Optional[str] = None):
        """
        """
        raise NotImplementedError
