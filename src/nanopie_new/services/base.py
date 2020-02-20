from abc import ABC, abstractmethod
from functools import partial, wraps
from typing import Callable, Dict, Optional

from ..handler import Handler, SimpleHandler

class RPCRequest(ABC):
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
                 extras: Optional[Dict] = None,
                 **kwargs):
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
                 serializer: 'Serializer',
                 authenticator: 'Authenticator',
                 logging_handler: 'LoggingHandler',
                 tracing_handler: 'TracingHandler',
                 max_content_length: int = 6000):
        """
        """
        self.endpoints = []
        self.serializer = serializer
        self.authenticator = authenticator
        self.logging_handler = logging_handler
        self.tracing_handler = tracing_handler
        self.max_content_length = max_content_length

    @abstractmethod
    def add_endpoint(self,
                     endpoint: RPCEndpoint,
                     **kwargs):
        """
        """
        pass
