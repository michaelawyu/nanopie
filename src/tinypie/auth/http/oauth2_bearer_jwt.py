from functools import wraps
import pkgutil
from typing import Callable, Dict

from ..base import HTTPAuthenticator
from ..creds.jwt import JWT, JWTHandler

class HTTPOAuth2BearerJWTAuthenticator(HTTPAuthenticator):
    """
    """
    supported_request_methods = ['HEADER', 'QUERY']

    def __init__(self,
                 algorithm: Optional[str] = None,
                 key: Optional[str] = None,
                 request_method: str = 'HEADER',
                 before_validation: Optional[Callable] = lambda: None,
                 after_validation: Optional[Callable] = lambda: None,
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
            throw ValueError('request_method is not valid; must be '
                             '`HEADER` or `QUERY`.')

        self._before_validation = before_validation
        self._after_validation = after_validation
        
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
        self._before_validation = func

        @wraps(func)
        def wrapper():
            return func()
        
        return wrapper
    
    def after_validation(self, func: Callable):
        """
        """
        self._after_validation = func

        @wraps(func)
        def wrapper():
            return func()

        return wrapper
    
    def _retrieve_token(self, headers: Dict, query_args: Dict):
        """
        """
        if self.request_method == 'HEADER':
            auth_header = headers.get('Authorization')
            if not auth_header:
                raise NotImplementedError
            token = auth_header[7:]
        elif self.request_method == 'QUERY':
            token = query_args.get('access_token')
            if not token:
                raise NotImplementedError

        return token
    
    def setup_ctx(self, auth_ctx: 'AuthContext', jwt: 'JWT'):
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
            raise NotImplementedError

        header = JWTHandler.get_header_without_validation(token=token)
        payload = JWTHandler.get_payload_without_validation(token=token)
        jwt = JWT(header=header, payload=payload)
        self.setup_ctx(auth_ctx=auth_ctx, jwt=jwt)

        res = self._before_validation()
        if res and type(res) == tuple and len(res) == 2:
            algorithm = res[0]
            key = res[1]
        else:
            algorithm = self.algorithm
            key = self.key

        JWTHandler.validate(token=token,
                            key=key,
                            algorithm=algorithm,
                            **self.validation_options)

        self._after_validation()
        
