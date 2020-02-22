from abc import abstractmethod
from typing import Callable, Dict, Optional

from ..base import RPCEndpoint, RPCRequest, RPCResponse, RPCService
from ...handler import Handler, SimpleHandler
from .methods import HTTPMethods

class HTTPRequest(RPCRequest):
    """
    """
    __slots__ = ('_url', '_headers', '_content_length', '_mime_type',
                 '_query_args', '_binary_data', '_text_data')

    def __init__(self,
                 url: Any[str, Callable],
                 headers: Any[Dict, Callable],
                 content_length: Any[int, Callable],
                 mime_type: Any[str, Callable],
                 query_args: Any[Dict, Callable],
                 binary_data: Callable,
                 text_data: Callable):
        """
        """
        self._url = url
        self._headers = headers
        self._content_length = content_length
        self._mime_type = mime_type
        self._query_args = query_args
        self._binary_data = binary_data
        self._text_data = text_data
    
    @staticmethod
    def _helper(v: Any) -> Any:
        """
        """
        if callable(v):
            return v()
        else:
            return v
    
    @property
    def url(self) -> str:
        return self._helper(self._url)
    
    @property
    def headers(self) -> Dict:
        return self._helper(self._headers)

    @property
    def content_length(self) -> int:
        return self._helper(self._content_length)
    
    @property
    def mime_type(self) -> str:
        return self._helper(self._mime_type)
    
    @property
    def query_args(self) -> Dict:
        return self._helper(self._query_args)
    
    @property
    def binary_data(self) -> bytes:
        return self._helper(self._binary_data)
    
    @property
    def text_data(self) -> str:
        return self._helper(self._text_data)

class HTTPResponse(RPCResponse):
    """
    """
    __slots__ = ('_url', '_status_code', '_headers', '_mime_type',
                 '_data')

    def __init__(self,
                 status_code: int = 200,
                 headers: Optional[Dict] = None,
                 mime_type: Optional[str] = None,
                 binary_data: Optional[bytes] = None,
                 text_data: Optional[str] = None):
        """
        """
        self._status_code = status_code
        self._headers = headers
        self._mime_type = mime_type
        if binary_data and text_data:
            raise RuntimeError('Fields binary_data and text_data are mutually '
                               'exclusive.')
        self._data = binary_data if binary_data else text_data

class HTTPEndpoint(RPCEndpoint):
    """
    """
    pass

class HTTPService(RPCService):
    """
    """
    def __init__(self,
                 serialization_handler: 'SerializationHandler', # To-Do 
                 authn_handler: Optional['AuthenticationHandler'] = None,
                 logging_handler: Optional['LoggingHandler'] = None,
                 tracing_handler: Optional['TracingHandler'] = None,
                 max_content_length: Optional[int] = 6000,
                 setup_tracing_as_middleware: bool = False):
        """
        """
        super().__init__(serialization_handler=serialization_handler,
                         authn_handler=authn_handler,
                         logging_handler=logging_handler,
                         tracing_handler=tracing_handler,
                         max_content_length=max_content_length)

    @abstractmethod
    def add_endpoint(self,
                     name: str,
                     rule: str,
                     entrypoint: Handler,
                     extras: Optional[Dict] = None,
                     **kwargs):
        pass
    
    def _rest_endpoint(self,
                       name: str,
                       rule: str,
                       method: str,
                       data_cls: Optional['ModelMetaKls'] = None,
                       headers_cls: Optional['ModelMetaKls'] = None,
                       query_cls: Optional['ModelMetaKls'] = None,
                       logging_context: Optional['ModelMetaKls'] = None,
                       serialization_handler: Optional['SerializationHandler'] = None,
                       authn_handler: Optional['AuthenticationHandler'] = None,
                       logging_handler: Optional['LoggingHandler'] = None,
                       tracing_handler: Optional['TracingHandler'] = None,
                       extras: Optional[Dict] = None,
                       **options):
        """
        """
        self.rules.append(rule, [method])

        # TO-DO
        raise NotImplementedError

    def create(self,
               name: str,
               rule: str,
               data_cls: 'ModelMetaKls',
               headers_cls: Optional['ModelMetaKls'] = None,
               query_cls: Optional['ModelMetaKls'] = None,
               logging_context: Optional['ModelMetaKls'] = None,
               serialization_handler: Optional['SerializationHandler'] = None,
               authn_handler: Optional['AuthenticationHandler'] = None,
               logging_handler: Optional['LoggingHandler'] = None,
               tracing_handler: Optional['TracingHandler'] = None,
               extras: Optional[Dict] = None,
               **options):
        """
        """
        return self._rest_endpoint(rule=rule,
                                   method=HTTPMethods.POST,
                                   data_cls=data_cls,
                                   headers_cls=headers_cls,
                                   query_cls=query_cls,
                                   logging_context=logging_context,
                                   serialization_handler=serialization_handler,
                                   authn_handler=authn_handler,
                                   logging_handler=logging_handler,
                                   tracing_handler=tracing_handler,
                                   extras=extras,
                                   **options)

    def add_create_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.create(*args, **kwargs)(func)    

    def get(self,
            name: str,
            rule: str,
            data_cls: Optional['ModelMetaKls'] = None,
            headers_cls: Optional['ModelMetaKls'] = None,
            query_cls: Optional['ModelMetaKls'] = None,
            logging_context: Optional['ModelMetaKls'] = None,
            serialization_handler: Optional['SerializationHandler'] = None,
            authn_handler: Optional['AuthenticationHandler'] = None,
            logging_handler: Optional['LoggingHandler'] = None,
            tracing_handler: Optional['TracingHandler'] = None,
            extras: Optional[Dict] = None,
            **options):
        """
        """
        return self._rest_endpoint(rule=rule,
                                   method=HTTPMethods.GET,
                                   data_cls=data_cls,
                                   headers_cls=headers_cls,
                                   query_cls=query_cls,
                                   logging_context=logging_context,
                                   serialization_handler=serialization_handler,
                                   authn_handler=authn_handler,
                                   logging_handler=logging_handler,
                                   tracing_handler=tracing_handler,
                                   extras=extras,
                                   **options)
    
    def add_get_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.get(*args, **kwargs)(func)
    
    def update(self,
               name: str,
               rule: str,
               data_cls: 'ModelMetaKls',
               headers_cls: Optional['ModelMetaKls'] = None,
               query_cls: Optional['ModelMetaKls'] = None,
               logging_context: Optional['ModelMetaKls'] = None,
               serialization_handler: Optional['SerializationHandler'] = None,
               authn_handler: Optional['AuthenticationHandler'] = None,
               logging_handler: Optional['LoggingHandler'] = None,
               tracing_handler: Optional['TracingHandler'] = None,
               extras: Optional[Dict] = None,
               **options):
        """
        """
        return self._rest_endpoint(rule=rule,
                                   method=HTTPMethods.PATCH,
                                   data_cls=data_cls,
                                   headers_cls=headers_cls,
                                   query_cls=query_cls,
                                   logging_context=logging_context,
                                   serialization_handler=serialization_handler,
                                   authn_handler=authn_handler,
                                   logging_handler=logging_handler,
                                   tracing_handler=tracing_handler,
                                   extras=extras,
                                   **options)
    
    def add_update_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.update(*args, **kwargs)(func)
    
    def delete(self,
               name: str,
               rule: str,
               data_cls: Optional['ModelMetaKls'] = None,
               headers_cls: Optional['ModelMetaKls'] = None,
               query_cls: Optional['ModelMetaKls'] = None,
               logging_context: Optional['ModelMetaKls'] = None,
               serialization_handler: Optional['SerializationHandler'] = None,
               authn_handler: Optional['AuthenticationHandler'] = None,
               logging_handler: Optional['LoggingHandler'] = None,
               tracing_handler: Optional['TracingHandler'] = None,
               extras: Optional[Dict] = None,
               **options):
        """
        """
        return self._rest_endpoint(rule=rule,
                                   method=HTTPMethods.DELETE,
                                   data_cls=data_cls,
                                   headers_cls=headers_cls,
                                   query_cls=query_cls,
                                   logging_context=logging_context,
                                   serialization_handler=serialization_handler,
                                   authn_handler=authn_handler,
                                   logging_handler=logging_handler,
                                   tracing_handler=tracing_handler,
                                   extras=extras,
                                   **options)

    def add_delete_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.delete(*args, **kwargs)(func)
    
    def list(self,
             name: str,
             rule: str,
             data_cls: Optional['ModelMetaKls'] = None,
             headers_cls: Optional['ModelMetaKls'] = None,
             query_cls: Optional['ModelMetaKls'] = None,
             logging_context: Optional['ModelMetaKls'] = None,
             serialization_handler: Optional['SerializationHandler'] = None,
             authn_handler: Optional['AuthenticationHandler'] = None,
             logging_handler: Optional['LoggingHandler'] = None,
             tracing_handler: Optional['TracingHandler'] = None,
             extras: Optional[Dict] = None,
             **options):
        """
        """
        return self._rest_endpoint(rule=rule,
                                   method=HTTPMethods.GET,
                                   data_cls=data_cls,
                                   headers_cls=headers_cls,
                                   query_cls=query_cls,
                                   logging_context=logging_context,
                                   serialization_handler=serialization_handler,
                                   authn_handler=authn_handler,
                                   logging_handler=logging_handler,
                                   tracing_handler=tracing_handler,
                                   extras=extras,
                                   **options)

    def add_list_endpoint(self, *args, func, **kwargs):
        """
        """
        return self.list(*args, **kwargs)(func)
    
    def custom(self,
               name: str,
               rule: str,
               verb: str,
               method: str,
               data_cls: Optional['ModelMetaKls'] = None,
               headers_cls: Optional['ModelMetaKls'] = None,
               query_cls: Optional['ModelMetaKls'] = None,
               logging_context: Optional['ModelMetaKls'] = None,
               serialization_handler: Optional['SerializationHandler'] = None,
               authn_handler: Optional['AuthenticationHandler'] = None,
               logging_handler: Optional['LoggingHandler'] = None,
               tracing_handler: Optional['TracingHandler'] = None,
               extras: Optional[Dict] = None,
               **options):
        """
        """
        if rule.endswith('/'):
            rule = rule[:-1]
        rule = '{}:{}'.format(rule, verb)

        if method not in HTTPMethods.all_methods:
            raise ValueError('{} is not a supported HTTP method ({}).'.format(
                                method, HTTPMethods.all_methods))

        return self._rest_endpoint(rule=rule,
                                   method=method,
                                   data_cls=data_cls,
                                   headers_cls=headers_cls,
                                   query_cls=query_cls,
                                   logging_context=logging_context,
                                   serialization_handler=serialization_handler,
                                   authn_handler=authn_handler,
                                   logging_handler=logging_handler,
                                   tracing_handler=tracing_handler,
                                   extras=extras,
                                   **options)
    
    def add_custom_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        self.custom(*args, **kwargs)(func)
