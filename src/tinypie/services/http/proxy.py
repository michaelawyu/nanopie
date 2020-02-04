from typing import Any, Callable, Dict, Optional

from ...auth.base import AuthContextBase
from .base import APIParams, ServiceContext

class ServiceContextProxy(ServiceContext):
    """
    """
    __slots__ = ('_proxy_func')

    def __init__(self, proxy_func: Callable):
        """
        """
        self._proxy_func = proxy_func
    
    def update_proxy_func(self, proxy_func: Callable):
        """
        """
        self._proxy_func = proxy_func

    @property
    def svc(self) -> 'HTTPService':
        """
        """
        return self._proxy_func().svc
    
    @property
    def api_params(self) -> 'APIParams':
        """
        """
        return self._proxy_func().api_params
    
    @property
    def auth_ctx(self) -> 'AuthContext':
        """
        """
        return self._proxy_func().auth_ctx

class APIParamsProxy(APIParams):
    """
    """
    __slots__ = ('_proxy_func')

    def __init__(self, proxy_func: Callable):
        """
        """
        self._proxy_func = proxy_func

    def update_proxy_func(self, proxy_func: Callable):
        """
        """
        self._proxy_func = proxy_func
    
    @property
    def body_params(self) -> 'ModelMetaKls':
        """
        """
        return self._proxy_func().body_params
    
    @property
    def query_params(self) -> 'QueryParameters':
        """
        """
        return self._proxy_func().query_params
    
    @property
    def header_params(self) -> 'HeaderParameters':
        """
        """
        return self._proxy_func().header_params
    
    @property
    def path_params(self) -> Dict:
        """
        """
        return self._proxy_func().path_params

class AuthContextProxy(AuthContextBase):
    """
    """
    __slots__ = ('_proxy_func')

    def __init__(self, proxy_func: Callable):
        """
        """
        self._proxy_func = proxy_func

    def update_proxy_func(self, proxy_func: Callable):
        """
        """
        self._proxy_func = proxy_func
    
    @property
    def jwt(self) -> 'JWT':
        """
        """
        return self._proxy_func().jwt
    
    @property
    def user_credential(self) -> 'HTTPBasicUserCredentail':
        """
        """
        return self._proxy_func().user_credential
    
    @property
    def api_key(self) -> 'APIKey':
        """
        """
        return self._proxy_func().api_key
