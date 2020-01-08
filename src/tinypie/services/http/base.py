from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

class HTTPServiceAbstract(ABC):
    """
    """
    @abstractmethod
    def endpoint(self,
                 resource: 'Resource',
                 rule: Optional[str] = None):
        """
        """
        return None
    
    @abstractmethod
    def create(self,
               resource: 'Resource',
               rule: Optional[str] = None):
        """
        """
        return None
    
    @abstractmethod
    def get(self,
            resource: 'Resource',
            rule: Optional[str] = None):
        """
        """
        return None

    @abstractmethod
    def update(self,
               resource: 'Resource',
               rule: Optional[str] = None):
        """
        """
        return None
    
    @abstractmethod
    def delete(self,
               resource: 'Resource',
               rule: Optional[str] = None):
        """
        """
        return None
    
    @abstractmethod
    def list(self,
             resource: 'Resource',
             rule: Optional[str] = None):
        """
        """
        return None

    @abstractmethod
    def add_resource(self, resource: 'Resource'):
        """
        """
        pass

class HTTPInputParametersAbstract(ABC):
    """
    """
    @abstractmethod
    def get_resource(self) -> 'Resource':
        pass

