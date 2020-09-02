"""This module includes the base classes for auth handlers and related objects.

An authentication handler authenticates a request automatically. It calls
a credential extractor first to extract from the request a credential
(if any), and then uses a credential validator to validate the credential.
If the credential is valid, the authentication handlers passes the baton
to a chained handler; otherwise it will return an error response.
"""

from abc import ABC, abstractmethod
from inspect import signature
from typing import Any, Callable, Optional

from ..globals import request as request_proxy
from ..handler import Handler
from ..services.base import Extractor


class Credential(ABC):
    """The base class for all credentials."""


class CredentialExtractor(Extractor):
    """The base class for all credential extractors.

    A credential extractor extracts a credential from a request. For example,
    an HTTP JWT credential extractor will read the `Authorization` HTTP header
    from an HTTP request and return a JWT credential.
    """

    @abstractmethod
    def extract(self, request: "RPCRequest") -> "Credential":
        """Extracts a credential from a request.

        Args:
            request (RPCRequest): A request.

        Returns:
            Credential: The extracted credential.
        """


class CredentialValidator(ABC):
    """The base class for all credential validators.

    A credential validator validates a credential. For example, an HTTP API key
    credential validator will accept a key credential, extracted by a
    credential extractor, and check if there is a matching record in a
    storage.
    """

    @abstractmethod
    def validate(self, credential: "Credential"):
        """Validates a credential.

        Args:
            credential (Credential): A credential.
        """


class AuthenticationHandler(Handler):
    """The base class for all authentication handlers."""

    def __init__(
        self,
        credential_extractor: "CredentialExtractor",
        credential_validator: Optional["CredentialValidator"],
    ):
        """Initializes an authentication handler.

        Args:
            credential_extractor (CredentialExtractor): A credential
                extractor.
            credential_validator (CredentialValidator, Optional): A credential
                validator. To prepare a credential validator dynamically at
                runtime, see the method `before_authentication`.
        """
        self._credential_extractor = credential_extractor
        self._credential_validator = credential_validator
        self._before_authentication = lambda auth_handler, credential: None
        self._after_authentication = lambda auth_handler, credential: None
        super().__init__()

    def __call__(self, *args, **kwargs) -> Any:
        """Runs the handler.

        It performs the following tasks:

        1. Call the extract method on the credential extractor to extract a
           credential from the request.
        2. If a before_authentication method is configured, run the method.
        3. If the before_authentication method returns a credential validator,
           calls the validate method on the credential validator to validate
           the extracted credential.

           Otherwise, use the credential validator specified in the initializer
           to validate the extracted credential.
        4. If the after_authentication method is configured, run the method.
        5. Pass the baton to the chained handler.

        Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary named arguments.

        Returns:
            Any: Any object.
        """
        credential = self._credential_extractor.extract(request=request_proxy)

        credential_validator = self._before_authentication(
            auth_handler=self, credential=credential
        )
        if not credential_validator:
            credential_validator = self._credential_validator

        credential_validator.validate(credential=credential)

        self._after_authentication(auth_handler=self, credential=credential)

        return super().__call__(*args, **kwargs)

    def before_authentication(self, func: Callable) -> Optional["CredentialValidator"]:
        """A decorator for setting up a before_authentication method.

        A before_authentication method allows developers to do some setup
        before the authentication starts. It may return a CredentialValidator,
        which the authentication handler will use for the authentication step
        (instead of the default one specified with the initializer, if there
        is any). A microservice/API service with JWT based authentication and
        rotated public keys, for example, may set up a before_authentication
        method that returns a CredentialValidator based on the specific
        public key the incoming JWT uses.

        The before_authentication method must have exactly two arguments,
        auth_handler and credential, which are a reference to the running
        auth handler and the incoming credential respectively.

        Usage:
        ```
        auth_handler = AuthenticationHandler(...)

        @auth_handler.before_validation
        def custom_before_validation(auth_handler, credential):
            # Do some setup
        ```
        """
        self._check_signature(func)
        self._before_authentication = func
        return func

    def after_authentication(self, func: Callable):
        """A decorator for setting up a after_authentication method.

        An after_authentication method allows developers to do some additional
        work after the authentication completes. A microservice/API service
        with JWT based authentication and custom JWT claims, for example,
        may set up a after_authentication method that verifies the custom
        claims as it sees fit.

        The after_authentication method must have exactly two arguments,
        auth_handler and credential, which are a reference to the running
        auth_handler and the incoming credential respectively.

        Usage:
        ```
        auth_handler = AuthenticationHandler(...)

        @auth_handler.after_authentication
        def custom_after_authentication(auth_handler, credential):
            # Do some additional work
        ```
        """
        self._check_signature(func)
        self._after_authentication = func
        return func

    @staticmethod
    def _check_signature(func: Callable):
        """Verifies the signature of before/after_authentication methods.

        Args:
            func (Callable): A before/after_authentication method.
        """
        if not callable(func):
            raise ValueError(
                "before_authentication and after_authentication "
                "must decorate a callable."
            )
        parameters = signature(func).parameters
        if (
            len(parameters) != 2
            or not parameters.get("auth_handler")
            or not parameters.get("credential")
        ):
            raise ValueError(
                "before_authentication and after_authentication "
                "must decorate a callable with two arguments "
                "named auth_handler and credential."
            )
