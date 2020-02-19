from functools import wraps
import inspect
import pkgutil
from typing import Callable, Dict, Optional

from ..base import HTTPAuthenticator
from ..creds.jwt import JWT, JWTHandler
from ...misc.errors import (
    HTTPOAuth2BearerHeaderMissingError,
    HTTPOAuth2BearerQueryArgMissingError,
    HTTPOAuth2BearerTokenNotFoundError,
    HTTPOAuth2BearerTokenInvalidError,
    InvalidJWTError
)

class HTTPOAuth2BearerJWTAuthenticator(HTTPAuthenticator):
    """
    """
    supported_request_methods = ['HEADER', 'QUERY']

    def __init__(self,
                 algorithm: Optional[str] = None,
                 key: Optional[str] = None,
                 request_method: str = 'HEADER',
                 before_validation: Optional[Callable] = None,
                 after_validation: Optional[Callable] = None,
                 use_cryptography: bool = True,
                 use_pycrypto: bool = False,
                 use_ecdsa: bool = False,
                 **validation_options):
        """
        """
        self.algorithm = algorithm
        self.key = key
        self.request_method = request_method
        if request_method not in self.supported_request_methods:
            raise ValueError(('request_method must be one of '
                              '{}').format(self.supported_request_methods))

        if not before_validation:
            before_validation = lambda header, payload: None
        self.before_validation(before_validation)
        if not after_validation:
            after_validation = lambda header, payload: None
        self.after_validation(after_validation)
        
        JWTHandler.check_dependencies(use_cryptography=use_cryptography,
                                      use_pycrypto=use_pycrypto,
                                      use_ecdsa=use_ecdsa)
        
        self.validation_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': True,
            'verify_iat': True,
            'verify_aud': False,
            'verify_iss': False,
            'require_exp': False,
            'require_iat': False,
            'require_nbf': False,
            'audience': None,
            'issuer': None,
            'leeway': 0
        }
        for k in validation_options:
            if k in self.validation_options:
                self.validation_options[k] = validation_options[k]
        
        if self.validation_options['verify_iss'] and \
           not self.validation_options['issuer']:
            raise ValueError('iss claim is required but no correct value is '
                            'present.')
        if self.validation_options['verify_aud'] and \
           not self.validation_options['audience']:
            raise ValueError('aud claim is required but no correct value is '
                             'present.')
    
    def before_validation(self, func: Callable):
        """
        """
        params = inspect.signature(func).parameters
        if len(params) != 2 or \
           'header' not in params or \
           'payload' not in params:
            raise ValueError('before_validation func must have two keyword '
                             'arguments, header and payload.')

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
           'header' not in params or \
           'payload' not in params:
            raise ValueError('after_validation func must have two keyword '
                             'arguments, header and payload.')

        self._after_validation = func

        @wraps(func)
        def wrapped():
            return func()

        return wrapped
    
    def _retrieve_token(self, headers: Dict, query_args: Dict):
        """
        """
        if self.request_method == 'HEADER':
            auth_header = headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer'):
                raise HTTPOAuth2BearerHeaderMissingError()
            token = auth_header[7:]
        elif self.request_method == 'QUERY':
            token = query_args.get('access_token')
            if not token:
                raise HTTPOAuth2BearerQueryArgMissingError()

        return token
    
    def _setup_ctx(self, auth_ctx: 'AuthContext', jwt: 'JWT'):
        """
        """
        auth_ctx.jwt = jwt

    def authenticate(self,
                     auth_ctx: 'AuthContext',
                     headers: Dict,
                     query_args: Dict):
        """
        """
        token = self._retrieve_token(headers, query_args)
        if not token:
            raise HTTPOAuth2BearerTokenNotFoundError()

        try:
            header = JWTHandler.get_header_without_validation(token=token)
            payload = JWTHandler.get_payload_without_validation(token=token)
        except InvalidJWTError as ex:
            raise HTTPOAuth2BearerTokenInvalidError(wrapped=ex)
        jwt = JWT(header=header, payload=payload)
        self._setup_ctx(auth_ctx=auth_ctx, jwt=jwt)

        res = self._before_validation(header=header, payload=payload)
        if res and type(res) == tuple and len(res) == 2:
            algorithm = res[0]
            key = res[1]
        else:
            algorithm = self.algorithm
            key = self.key

        try:
            JWTHandler.validate(token=token,
                                key=key,
                                algorithm=algorithm,
                                **self.validation_options)
        except InvalidJWTError as ex:
            raise HTTPOAuth2BearerTokenInvalidError(wrapped=ex)

        self._after_validation(header=header, payload=payload)
