from abc import ABC, abstractmethod
from typing import Callable, Dict

class HTTPAuthenticator(ABC):
    """
    """
    @abstractmethod
    def authenticate(self,
                     headers: Callable,
                     query_args: Callable):
        """
        """
        pass

class AuthContext():
    """
    """
    def __init__(self):
        """
        """
        raise NotImplementedError

    @property
    def jwt(self):
        """
        """
        raise NotImplementedError
