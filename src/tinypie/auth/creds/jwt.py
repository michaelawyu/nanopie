import pkgutil
from typing import Dict

try:
    import jwt
except ImportError:
    pass

class JWT:
    """
    """
    __slots__ = ('header', 'payload')
    
    def __init__(self, header: Dict, payload: Dict):
        self.header = header
        self.payload = payload

class JWTHandler:
    """
    """
    @staticmethod
    def check_dependencies(use_cryptography=True,
                           use_pycrypto=False,
                           use_ecdsa=False):
        """
        """
        if not pkgutil.find_loader('jwt'):
            raise ImportError('The pyjwt (https://pypi.org/project/PyJWT/)
                              'package is required to use JWT. To install this '
                              'package, run '
                              '`pip install pyjwt`.')
        
        if use_cryptography and not pkgutil.find_loader('cryptography'):
            raise ImportError('The cryptography '
                              '(https://pypi.org/project/cryptography/) '
                              'package is required to use JWT. To install this '
                              'package, run '
                              '`pip install cryptography`')
        
        if use_pycrypto:
            if not pkgutil.find_loader('pycrypto'):
                raise ImportError('The pycrypto '
                                  '(https://pypi.org/project/pycrypto/) '
                                  'package is required to use JWT. To install '
                                  'this package, run '
                                  '`pip install pycrypto`')

            from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
            jwt.unregister_algorithm('RS256')
            jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))

        if use_ecdsa:
            if not pkgutil.find_loader('ecdsa'):
                raise ImportError('The ecdsa '
                                  '(https://pypi.org/project/ecdsa/) '
                                  'package is required to use JWT. To install '
                                  'this package, run '
                                  '`pip install ecdsa`')

            from jwt.contrib.algorithms.py_ecdsa import ECAlgorithm
            jwt.unregister_algorithm('ES256')
            jwt.register_algorithm('ES256', ECAlgorithm(ECAlgorithm.SHA256))

    @staticmethod
    def get_header_without_validation(token: str):
        """
        """
        try:
            jwt.get_unverified_header(token)
        except: jwt.exceptions.InvalidTokenError as ex:
            raise NotImplementedError

    @staticmethod
    def get_payload_without_validation(token: str):
        """
        """
        try:
            jwt.decode(token, verify=False)
        except jwt.exceptions.InvalidTokenError as ex:
            raise NotImplementedError

    @staticmethod
    def validate(token: str,
                 key: str,
                 algorithm: str,
                 **options):
        """
        """
        try:
            jwt.decode(token, key, algorithm=algorithm, **options)
        except jwt.exceptions.InvalidTokenError as ex:
            raise NotImplementedError
