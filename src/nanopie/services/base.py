from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..handler import Handler

class RPCRequest(ABC):
    """
    """

class Extractor(ABC):
    """
    """
    @abstractmethod
    def extract(self, request: 'RPCRequest') -> Any:
        """
        """

class RPCResponse(ABC):
    """
    """

class RPCEndpoint(ABC):
    """
    """
    def __init__(self,
                 name: str,
                 rule: str,
                 entrypoint: Handler,
                 extras: Optional[Dict] = None):
        """
        """
        self.name = name
        self.rule = rule
        self.entrypoint = entrypoint
        self.extras = extras

class RPCService(ABC):
    """
    """
    def __init__(self,
                 serialization_handler: 'SerializationHandler',
                 authn_handler: 'AuthenticationHandler',
                 logging_handler: 'LoggingHandler',
                 tracing_handler: 'TracingHandler',
                 max_content_length: int = 6000):
        """
        """
        self.endpoints = []
        self.serialization_handler = serialization_handler
        self.authn_handler = authn_handler
        self.logging_handler = logging_handler
        self.tracing_handler = tracing_handler
        self.max_content_length = max_content_length

    @abstractmethod
    def add_endpoint(self,
                     endpoint: RPCEndpoint,
                     **kwargs):
        """
        """
