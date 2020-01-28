import pkgutil
from typing import Callable, Dict, Optional

try:
    import jwt
except ImportError:
    raise ImportError(
        'The pyjwt (https://pypi.org/project/PyJWT/) package is required to '
        'use OAuth2 Bearer Token based authentication (RFC 6750) with '
        'JWT (RFC 7519). To install this package, run '
        '`pip install pyjwt`.'
    )

from ..base import Authenticator

CRYPTOGRAPHY_INSTALLED = True if pkgutil.find_loader('cryptography') else False
PYCRYPTO_INSTALLED = True if pkgutil.find_loader('pycrypto') else False
ECDSA_INSTALLED = True if pkgutil.find_loader('ecdsa') else False

SUPPORTED_ALGORITHMS = ['HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512',
                        'ES256', 'ES384', 'ES512', 'PS256', 'PS384', 'PS512']

class OAuth2BearerJWTSimpleAuthenticator(Authenticator):
    """
    """
    def __init__(self,
                 algorithm: str,
                 key: Optional[str] = None,
                 use_legacy_crypto_libs: bool = False,
                 custom_claims_verification: Optional[Callable] = None,
                 **kwargs):
        """
        """
        if algorithm not in SUPPORTED_ALGORITHMS:
            raise ValueError('Specified algorithm is not supported.')

        if use_legacy_crypto_libs:
            if algorithm.startswith('RS') and PYCRYPTO_INSTALLED:
                jwt.unregister_algorithm(algorithm)

                from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
                jwt.register_algorithm(algorithm,
                    RSAAlgorithm(getattr(RSAAlgorithm, 'SHA' + algorithm[2:])))
            elif algorithm.startswith('ES') and ECDSA_INSTALLED:
                jwt.unregister_algorithm(algorithm)

                from jwt.contrib.algorithms.py_ecdsa import ECAlgorithm
                jwt.unregister_algorithm(algorithm,
                    ECAlgorithm(getattr(ECAlgorithm, 'SHA' + algorithm[2:])))
            else:
                raise ValueError('Specified algorithm is not supported by '
                                 'legacy libraries, or legacy libraries '
                                 'are not installed.')
        elif not CRYPTOGRAPHY_INSTALLED:
            raise ValueError('The cryptography '
                             '(https://pypi.org/project/cryptography/) package '
                             'is required to use OAuth2 Bearer Token based '
                             'authentication. To install this package, run '
                             '`pip install cryptography`.')
        
        if algorithm.startswith('HS') and not secret:
            raise ValueError('A secret is required to use HMAC algorithms.')
        elif not algorithm.startswith('HS') and not public_key:
            raise ValueError('A public key is required to use asymmetric '
                             'algorithms.')
        
        self.algorithm = algorithm
        self.key = key
        if custom_claims_verification:
            self.custom_claims_verification = custom_claims_verification
        else:
            self.custom_claims_verification = lambda payload: None

        options = {
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
        for k in kwargs:
            if options.get(k):
                options[k] = kwargs[k]
        
        if options.get('verify_iss') and not options.get('issuer')):
            raise NotImplementedError
        elif options.get('verify_aud') and not options.get('audience')):
            raise 
        
        self.options = options

    def authenticate(self,
                     headers: Dict,
                     query_args: Dict):
        """
        """
        auth_header = headers.get('Authorization')
        if not auth_header:
            raise NotImplementedError
        token = auth_header[7:]
        try:
            jwt.decode(token, self.key, **self.options)
        except jwt.exceptions.InvalidTokenError as ex:
            raise NotImplementedError
