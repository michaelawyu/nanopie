"""This module includes the classes for nanopie services and related objects.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..handler import Handler


class RPCRequest(ABC):
    """The base class for all requests."""


class RPCParsedRequest(ABC):
    """The base class for all parsed requests."""


class Extractor(ABC):
    """The base class for all extractors."""

    @abstractmethod
    def extract(self, request: "RPCRequest") -> Any:
        """Extracts from a request."""


class RPCResponse(ABC):
    """The base class for all responses."""


class RPCEndpoint(ABC):
    """The base class for all endpoints."""

    def __init__(
        self, name: str, rule: str, entrypoint: Handler, extras: Optional[Dict] = None
    ):
        """Initializes an endpoint.

        Args:
            name (str): The name of the entrypoint.
            rule (str): The rule associated with the endpoint.
            entrypoint (Handler): The handler used as entrypoint.
            extras (Dict, Optional): Additional information about the endpoint.
        """
        self.name = name
        self.rule = rule
        self.entrypoint = entrypoint
        self.extras = extras


class RPCService(ABC):
    """The base class for all services."""

    def __init__(
        self,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        serialization_helper: Optional["SerializationHelper"] = None,
        max_content_length: int = 6000,
    ):
        """Initializes a service.

        Args:
            authn_handler (AuthenticationHandler, Optional): The default
                authentication handler for endpoints.
            logging_handler (LoggingHandler, Optional): The default logging
                handler for endpoints.
            tracing_handler (TracingHandler, Optional): The default tracing
                handler for endpoints.
            serialization_helper (SerializationHelper, Optional): The
                default serialization helper for endpoints.
            max_content_length (int): The maximum length of requests.
        """
        self.endpoints = {}
        self.authn_handler = authn_handler
        self.logging_handler = logging_handler
        self.tracing_handler = tracing_handler
        self.serialization_helper = serialization_helper
        self.max_content_length = max_content_length

    @abstractmethod
    def add_endpoint(self, endpoint: RPCEndpoint, **kwargs):
        """Adds an endpoint.

        Args:
            endpoint (RPCEndpoint): An endpoint.
            **kwrags: Arbitrary keyword arguments.
        """
