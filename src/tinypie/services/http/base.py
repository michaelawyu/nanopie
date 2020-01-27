from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

class HTTPService(ABC):
    """
    """
    @abstractmethod
    def endpoint(self,
                 rule: str,
                 methods: List[str],
                 body_params_cls: 'ModelMetaKls',
                 query_param_cls: 'ModelMetaKls',
                 header_param_cls: 'ModelMetaKls',
                 **options):
        """
        """
        return None
    
    @abstractmethod
    def create(self,
               rule: str,
               body_params_cls: 'ModelMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               **options):
        """
        """
        return None
    
    @abstractmethod
    def get(self,
            rule: str,
            body_params_cls: 'ModelMetaKls',
            query_param_cls: 'ModelMetaKls',
            header_param_cls: 'ModelMetaKls',
            **options):
        """
        """
        return None

    @abstractmethod
    def update(self,
               rule: str,
               body_params_cls: 'ModelMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               **options):
        """
        """
        return None
    
    @abstractmethod
    def delete(self,
               rule: str,
               body_params_cls: 'ModelMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               **options):
        """
        """
        return None
    
    @abstractmethod
    def list(self,
             rule: str,
             body_params_cls: 'ModelMetaKls',
             query_param_cls: 'ModelMetaKls',
             header_param_cls: 'ModelMetaKls',
             **options):
        """
        """
        return None
    
    @abstractmethod
    def custom(self,
               rule: str,
               verb: str,
               method: str,
               body_params_cls: 'ModelMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               **options):
        """
        """
        return None

class ServiceContext(ABC):
    """
    """
    @property
    @abstractmethod
    def api_params(self) -> 'APIParams':
        """
        """
        return None

    @property
    @abstractmethod
    def svc(self) -> 'HTTPService':
        """
        """
        return None

class APIParams(ABC):
    """
    """
    @property
    @abstractmethod
    def body_params(self) -> 'Model':
        """
        """
        return None

    @property
    @abstractmethod
    def query_params(self) -> 'QueryParameters':
        """
        """
        return None

    @property
    @abstractmethod
    def header_params(self) -> 'HeaderParameters':
        """
        """
        return None

    @property
    @abstractmethod
    def path_params(self) -> Dict:
        """
        """
        return {}

