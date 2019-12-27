from abc import ABC, abstractmethod
from typing import Any, Callable

class HTTPServiceAbstract(ABC):
    """
    """

    @abstractmethod
    def endpoint(self, func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def create(self, func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def get(self, func: Callable) -> Callable:
        """
        """
        return func

    @abstractmethod
    def update(self, func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def delete(self, func: Callable) -> Callable:
        """
        """
        return func
    
    @abstractmethod
    def list(self, func: Callable) -> Callable:
        """
        """
        return func
