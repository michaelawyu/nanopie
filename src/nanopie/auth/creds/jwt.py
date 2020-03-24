import pkgutil

try:
    import jwt

    JWT_INSTALLED = True
except ImportError:
    JWT_INSTALLED = False

from ..base import Credential, CredentialValidator
from ...misc.errors import AuthenticationError

PYCRYPTO_SUPPORTED_ALGS = ["RS256", "RS384", "RS512"]
ECDSA_SUPPORTED_ALGS = ["ES256", "ES384", "ES512"]


class JWT(Credential):
    """
    """

    __slots__ = ("header", "payload")

    def __init__(self, token: str):
        """
        """
        if not JWT_INSTALLED:
            raise ImportError(
                "The pyjwt (https://pypi.org/project/PyJWT/)"
                "package is required to use JWTs. To "
                "install this package, run "
                "`pip install pyjwt`."
            )
        self.token = token
        try:
            self.header = jwt.get_unverified_header(token)
            self.payload = jwt.decode(token, verify=False)
        except jwt.exceptions.InvalidTokenError as ex:
            message = "The provided JWT is not valid ({})".format(str(ex))
            raise AuthenticationError(message)


class JWTValidator(CredentialValidator):
    """
    """

    def __init__(
        self,
        key_or_secret: str,
        algorithm: str,
        use_pycrypto: bool = False,
        use_ecdsa: bool = False,
        **kwargs
    ):
        """
        """
        if not JWT_INSTALLED:
            raise ImportError(
                "The pyjwt (https://pypi.org/project/PyJWT/)"
                "package is required to validate JWTs. To "
                "install this package, run "
                "`pip install pyjwt`."
            )

        self._key = key_or_secret
        self._algorithm = algorithm

        if use_pycrypto:
            if algorithm not in PYCRYPTO_SUPPORTED_ALGS:
                raise ValueError("pycrypto does not support the specified " "algorithm.")
            if not pkgutil.find_loader("Crypto"):
                raise ImportError(
                    "The pycrypto "
                    "(https://pypi.org/project/pycrypto/) "
                    "package is required to validation JWTs. "
                    "To install this package, run "
                    "`pip install pycrypto`"
                )

            from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

            jwt.unregister_algorithm(algorithm)
            jwt.register_algorithm(algorithm, RSAAlgorithm(getattr(RSAAlgorithm, 'SHA' + algorithm[2:])))
        elif use_ecdsa:
            if algorithm not in ECDSA_SUPPORTED_ALGS:
                raise ValueError("ecdsa does not support the specified " "algorithm.")
            if not pkgutil.find_loader("ecdsa"):
                raise ImportError(
                    "The ecdsa "
                    "(https://pypi.org/project/ecdsa/) "
                    "package is required to validate JWTs. "
                    "To install this package, run "
                    "`pip install ecdsa`"
                )
            from jwt.contrib.algorithms.py_ecdsa import ECAlgorithm

            jwt.unregister_algorithm(algorithm)
            jwt.register_algorithm(algorithm, ECAlgorithm(getattr(ECAlgorithm, 'SHA' + algorithm[2:])))
        elif not pkgutil.find_loader("cryptography"):
            raise ImportError(
                "The cryptography "
                "(https://pypi.org/project/cryptography/) "
                "package is required to validate JWTs. "
                "To install this package, run "
                "`pip install cryptography`"
            )

        self._validation_options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_nbf": True,
            "verify_iat": True,
            "verify_aud": False,
            "verify_iss": False,
            "require_exp": False,
            "require_iat": False,
            "require_nbf": False
        }

        self._canonical_info = {
            "audience": None,
            "issuer": None,
            "leeway": 0
        }

        for k in kwargs:
            if k in self._validation_options:
                self._validation_options[k] = kwargs[k]
            elif k in self._canonical_info:
                self._canonical_info[k] = kwargs[k]

        if (
            self._validation_options["verify_iss"]
            and not self._canonical_info["issuer"]
        ):
            raise ValueError("No expected issuer.")

        if (
            self._validation_options["verify_aud"]
            and not self._canonical_info["audience"]
        ):
            raise ValueError("No expected audience.")

    def validate(self, credential: "JWT"):
        """
        """
        try:
            jwt.decode(
                credential.token,
                self._key,
                algorithms=self._algorithm,
                options=self._validation_options,
                **self._canonical_info
            )
        except jwt.exceptions.InvalidTokenError as ex:
            message = "The provided JWT is not valid ({})".format(str(ex))
            raise AuthenticationError(message)
