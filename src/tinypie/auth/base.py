from abc import ABC, abstractmethod
from typing import Dict

class Authenticator(ABC):
    """
    """
    @abstractmethod
    def authenticate(self,
                     headers: Dict,
                     query_args: Dict):
        """
        """
        pass
