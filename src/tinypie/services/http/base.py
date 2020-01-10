from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

class HTTPServiceAbstract(ABC):
    """
    """
    @abstractmethod
    def endpoint(self,
                 resource_cls: 'ResourceMetaKls',
                 query_param_cls: 'ModelMetaKls',
                 header_param_cls: 'ModelMetaKls',
                 rule: Optional[str] = None):
        """
        """
        return None
    
    @abstractmethod
    def create(self,
               resource_cls: 'ResourceMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str] = None,
               **options):
        """
        """
        return None
    
    @abstractmethod
    def get(self,
            resource_cls: 'ResourceMetaKls',
            query_param_cls: 'ModelMetaKls',
            header_param_cls: 'ModelMetaKls',
            rule: Optional[str] = None,
            **options):
        """
        """
        return None

    @abstractmethod
    def update(self,
               resource_cls: 'ResourceMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str] = None,
               **options):
        """
        """
        return None
    
    @abstractmethod
    def delete(self,
               resource_cls: 'ResourceMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str] = None,
               **options):
        """
        """
        return None
    
    @abstractmethod
    def list(self,
             resource_cls: 'ResourceMetaKls',
             query_param_cls: 'ModelMetaKls',
             header_param_cls: 'ModelMetaKls',
             rule: Optional[str] = None,
             **options):
        """
        """
        return None
    
    @abstractmethod
    def custom(self,
               resource_cls: 'ResourceMetaKls',
               verb: str,
               method: str,
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str] = None,
               **options):
        """
        """
        return None

    @abstractmethod
    def add_resource(self, resource_cls: 'ResourceMetaKls'):
        """
        """
        pass

class HTTPInputParametersAbstract(ABC):
    """
    """
    @abstractmethod
    def get_resource(self) -> 'Resource':
        """
        """
        return None

    @abstractmethod
    def get_query_parameters(self) -> 'QueryParameters':
        """
        """
        return None

    @abstractmethod
    def get_header_parameters(self) -> 'HeaderParameters':
        """
        """
        return None

    @abstractmethod
    def get_path_parameters(self) -> Dict:
        """
        """
        return {}

