from abc import ABC, abstractmethod
from typing import Any, Callable

from ...entities.model import Model

class HTTPServiceAbstract(ABC):
    """
    """

    @abstractmethod
    def endpoint(self,
                 resource: Model,
                 func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def create(self,
               resource: Model,
               func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def get(self,
            resource: Model,
            func: Callable) -> Callable:
        """
        """
        return func

    @abstractmethod
    def update(self,
               resource: Model,
               func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def delete(self,
               resource: Model,
               func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def list(self,
             resource: Model,
             func: Callable) -> Callable:
        """
        """
        return func

    @abstractmethod
    def add_resource(self, resource: Model):
        """
        """
        pass
