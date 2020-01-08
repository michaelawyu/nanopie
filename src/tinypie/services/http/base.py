from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

class HTTPServiceAbstract(ABC):
    """
    """

    @abstractmethod
    def endpoint(self,
                 resource: 'Resource',
                 path: Optional[str] = None):
        """
        """
        return func
    
    @abstractmethod
    def create(self,
               resource: 'Resource',
               path: Optional[str] = None):
        """
        """
        return func
    
    @abstractmethod
    def get(self,
            resource: 'Resource',
            path: Optional[str] = None):
        """
        """
        return func

    @abstractmethod
    def update(self,
               resource: 'Resource',
               path: Optional[str] = None):
        """
        """
        return func
    
    @abstractmethod
    def delete(self,
               resource: 'Resource',
               path: Optional[str] = None):
        """
        """
        return func
    
    @abstractmethod
    def list(self,
             resource: 'Resource',
             path: Optional[str] = None):
        """
        """
        return func

    @abstractmethod
    def add_resource(self, resource: 'Resource'):
        """
        """
        pass
