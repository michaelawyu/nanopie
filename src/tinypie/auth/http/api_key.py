from typing import Callable

from ..base import HTTPAuthenticator
from ..creds.api_key import APIKey
from ...misc.errors import (
    HTTPAPIKeyAuthHeaderMissingError,
    HTTPAPIKeyAuthQueryArgMissingError
)

class HTTPAPIKeyAuthentication(HTTPAuthenticator):
    """
    """
    supported_request_methods = ['HEADER', 'QUERY']

    def __init__(self,
                 request_method: str,
                 param_name: str,
                 validation_handler: Optional[Callable] = None,
                 before_validation: Optional[Callable] = None,
                 after_validation: Optional[Callable] = None):
        """
        """
        if request_method not in self.supported_request_methods:
            raise ValueError(('request_method must be one of '
                              '{}').format(self.supported_request_methods))
        self.request_method = request_method
        self.param_name = param_name

        def validation_handler_default(api_key: str):
            raise NotImplementedError('A validation handler is required.')

        if not validation_handler:
            self.validation_handler(validation_handler_default)

        if not before_validation:
            before_validation = lambda api_key: None
        self.before_validation(before_validation)
        if not after_validation:
            after_validation = lambda api_key: None
        self.after_validation(after_validation)
    
    def validation_handler(self, func: Callable):
        """
        """
        params = inspect.signature(func).parameters
        if len(params) != 1 or \
           'api_key' not in params:
            raise ValueError('validation_handler func must have one keyword '
                             'arguments, api_key.')
        
        self._validation_handler = func

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    def before_validation(self, func: Callable):
        """
        """
        params = inspect.signature(func).parameters
        if len(params) != 1 or \
           'api_key' not in params:
            raise ValueError('before_validation func must have one keyword '
                             'arguments, api_key.')
        
        self._before_validation = func

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped
    
    def after_validation(self, func: Callable):
        """
        """
        params = inspect.signature(func).parameters
        if len(params) != 1 or \
           'api_key' not in params:
            raise ValueError('after_validation func must have one keyword '
                             'arguments, api_key.')
        
        self._after_validation = func

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    def _retrieve_api_key(self, headers: Dict, query_args: Dict):
        """
        """
        if self.request_method == 'HEADER':
            api_key = headers.get(self.param_name)
            if not api_key:
                raise HTTPAPIKeyAuthHeaderMissingError
        elif self.request_method == 'QUERY':
            api_key = query_args.get(self.param_name)
            if not api_key:
                raise HTTPAPIKeyAuthQueryArgMissingError

        return api_key
    
    def _setup_ctx(self,
                   auth_ctx: 'AuthContext',
                   api_key: 'APIKey'):
        """
        """
        auth_ctx.api_key = api_key

    def authenticate(self,
                     auth_ctx: 'AuthContext',
                     headers: Dict,
                     query_args: Dict):
        """
        """
        api_key = self._retrieve_api_key(headers, query_args)
        
        self._setup_ctx(auth_ctx=auth_ctx,
                        api_key=APIKey(key=key))

        self._before_validation(api_key=api_key)
        self._validation_handler(api_key=api_key)
        self._after_validation(api_key=api_key)
