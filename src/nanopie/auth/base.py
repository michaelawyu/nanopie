from abc import ABC, abstractmethod
from inspect import signature
from typing import Callable, Optional

from ..globals import request as request_proxy
from ..handler import Handler
from ..services.base import Extractor


class Credential(ABC):
    """
    """


class CredentialExtractor(Extractor):
    """
    """

    @abstractmethod
    def extract(self, request: "RPCRequest") -> "Credential":
        """
        """


class CredentialValidator(ABC):
    """
    """

    @abstractmethod
    def validate(self, credential: "Credential"):
        """
        """


class AuthenticationHandler(Handler):
    """
    """

    def __init__(
        self,
        credential_extractor: "CredentialExtractor",
        credential_validator: "CredentialValidator",
    ):
        """
        """
        self._credential_extractor = credential_extractor
        self._credential_validator = credential_validator
        self._before_authentication = lambda: None
        self._after_authentication = lambda: None
        super().__init__()

    def __call__(self, *args, **kwargs):
        """
        """
        credential = self._credential_extractor.extract(request=request_proxy)

        credential_validator = self._before_authentication(self)
        if not credential_validator:
            credential_validator = self._credential_validator

        credential_validator.validate(credential=credential)

        self._after_authentication(self)

        return super().__call__(*args, **kwargs)

    def before_authentication(self, func: Callable) -> Optional["CredentialValidator"]:
        """
        """
        self._check_signature(func)
        self._before_authentication = func
        return func

    def after_authentication(self, func: Callable):
        """
        """
        self._check_signature(func)
        self._after_authentication = func
        return func

    @staticmethod
    def _check_signature(func: Callable):
        """
        """
        if not callable(func):
            raise ValueError(
                "before_authentication and after_authentication "
                "must decorate a callable."
            )
        parameters = signature(func).parameters
        if len(parameters) != 1 or not parameters.get("auth_handler"):
            raise ValueError(
                "before_authentication and after_authentication "
                "must decorate a callable with exactly one"
                "argument named auth_handler."
            )
