from abc import ABC, abstractmethod
from typing import Callable, Dict

class HTTPAuthenticator(ABC):
    """
    """
    @abstractmethod
    def before_validation(self, func: Callable):
        """
        """
        pass

    @abstractmethod
    def after_validation(self, func: Callable):
        """
        """
        pass

    @abstractmethod
    def authenticate(self,
                     auth_ctx: 'AuthContext',
                     headers: Dict,
                     query_args: Dict):
        """
        """
        pass

class AuthContextBase(ABC):
    """
    """
    @property
    @abstractmethod
    def jwt(self) -> 'JWT':
        """
        """
        return None
    
    @property
    @abstractmethod
    def user_credential(self) -> 'HTTPBasicUserCredential':
        """
        """
        return None
    
    @property
    @abstractmethod
    def api_key(self) -> 'APIKey':
        """
        """
        return None

class AuthContext:
    """
    """
    __slots__ = ('_jwt', '_user_credential', '_api_key')

    def __init__(self):
        """
        """
        self._jwt = None
        self._user_credential = None
        self._api_key = None
    
    @property
    def jwt(self) -> 'JWT':
        """
        """
        return self._jwt
    
    @jwt.setter
    def jwt(self, jwt: 'JWT'):
        """
        """
        self._jwt = jwt
    
    @property
    def user_credential(self) -> 'HTTPBasicUserCredentail':
        """
        """
        return self._user_credential
    
    @user_credential.setter
    def user_credential(self, user_credential: 'HTTPBasicUserCredential'):
        """
        """
        self._user_credential = user_credential
    
    @property
    def api_key(self) -> 'APIKey':
        """
        """
        return self._api_key
    
    @api_key.setter
    def api_key(self, api_key: 'APIKey'):
        """
        """
        self._api_key = api_key
