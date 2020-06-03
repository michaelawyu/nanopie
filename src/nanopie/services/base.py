from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..handler import Handler


class RPCRequest(ABC):
    """
    """


class RPCParsedRequest(ABC):
    """
    """


class Extractor(ABC):
    """
    """

    @abstractmethod
    def extract(self, request: "RPCRequest") -> Any:
        """
        """


class RPCResponse(ABC):
    """
    """


class RPCEndpoint(ABC):
    """
    """

    def __init__(
        self, name: str, rule: str, entrypoint: Handler, extras: Optional[Dict] = None
    ):
        """
        """
        self.name = name
        self.rule = rule
        self.entrypoint = entrypoint
        self.extras = extras


class RPCService(ABC):
    """
    """

    def __init__(
        self,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        serialization_helper: Optional["SerializationHelper"] = None,
        max_content_length: int = 6000,
    ):
        """
        """
        self.endpoints = {}
        self.authn_handler = authn_handler
        self.logging_handler = logging_handler
        self.tracing_handler = tracing_handler
        self.serialization_helper = serialization_helper
        self.max_content_length = max_content_length

    @abstractmethod
    def add_endpoint(self, endpoint: RPCEndpoint, **kwargs):
        """
        """
