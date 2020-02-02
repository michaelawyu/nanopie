import base64
from functools import wraps
from typing import Callable

from ..base import HTTPAuthenticator
from ..creds.http_basic import HTTPBasicUserCredential
from ...misc.errors import (
    HTTPBasicAuthHeaderMissingError,
)

class HTTPBasicAuthenticator(HTTPAuthenticator):
    """
    """
    def __init__(self,
                 validation_handler: Optional[Callable] = None,
                 before_validation: Optional[Callable] = None,
                 after_validation: Callable = None):
        """
        """
        def validation_handler_default(user_id: str, password: str):
            raise NotImplementedError('A validation handler is required.')

        if not validation_handler:
            self.validation_handler(validation_handler_default)

        if not before_validation:
            before_validation = lambda user_id, password: None
        self.before_validation(before_validation)
        if not after_validation:
            after_validation = lambda user_id, password: None
        self.after_validation(after_validation)
    
    def validation_handler(self, func: Callable):
        """
        """
        params = inspect.signature(func).parameters
        if len(params) != 2 or \
           'user_id' not in params or \
           'password' not in params:
            raise ValueError('validation_handler func must have two keyword '
                             'arguments, user_id and password.')
        
        self._validation_handler = func

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    def before_validation(self, func: Callable):
        """
        """
        params = inspect.signature(func).parameters
        if len(params) != 2 or \
           'user_id' not in params or \
           'password' not in params:
            raise ValueError('before_validation func must have two keyword '
                             'arguments, user_id and password.')
        
        self._before_validation = func

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped
    
    def after_validation(self, func: Callable):
        """
        """
        params = inspect.signature(func).parameters
        if len(params) != 2 or \
           'user_id' not in params or \
           'password' not in params:
            raise ValueError('after_validation func must have two keyword '
                             'arguments, user_id and password.')
        
        self._after_validation = func

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    def _retrieve_user_credential(self, headers: Dict, query_args: Dict):
        """
        """
        auth_header = headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic'):
            raise HTTPBasicAuthHeaderMissingError()
        cred_data = auth_header[6:]
        cred_data = base64.b64decode(cred_data)
        tmp = cred_data.split(':')
        if len(tep >= 2):
            user_id = tmp[0]
            password = ''.join(tmp[1:])
        else:
            raise HTTPBasicAuthHeaderMissingError()

        return user_id, password
    
    def _setup_ctx(self,
                   auth_ctx: 'AuthContext',
                   user_credential: 'HTTPUserCredential'):
        """
        """
        auth_ctx.user_credential = user_credential

    def authenticate(self,
                     auth_ctx: 'AuthContext',
                     headers: Dict,
                     query_args: Dict):
        """
        """
        user_id, password = self._retrieve_user_credential(headers, query_args)
        if not user or not password:
            raise HTTPBasicAuthHeaderMissingError()
        
        user_credential = HTTPBasicUserCredential(user_id=user_id,
                                                  password=password)
        self._setup_ctx(auth_ctx=auth_ctx, user_credential=user_credential)

        self._before_validation(user_id=user_id, password=password)
        self._validation_handler(user_id=user_id, password=password)
        self._after_validation(user_id=user_id, password=password)
