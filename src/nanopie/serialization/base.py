"""This module includes the base classes for serialization handlers.

A serialization handler helps serialization and deserialization. When
configured with an endpoint in a microservice/API service, it automatically
deserializes requests payloads into models every time a request arrives;
if the endpoint returns models as responses, the handler will also serializes
them. Serialization handlers use helpers (`SerializationHelper`) to support
different serialization formats.
"""

from abc import abstractmethod
from typing import Any

from ..handler import Handler


class SerializationHandler(Handler):
    """The base class for all serialization handlers."""

    def __init__(self, serialization_helper: "SerializationHelper"):
        """Initializes a serialization handler.

        Args:
            serialization_helper (SerializationHelper): a serialization
                helper.
        """
        self._serialization_helper = serialization_helper

        super().__init__()

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        """Runs the serialization handler.

        Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary named arguments.

        Returns:
            Any: Any object.
        """
        return super().__call__(*args, **kwargs)
