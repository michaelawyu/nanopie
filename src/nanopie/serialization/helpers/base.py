"""This module includes the base class for serialization helpers.

A serialization helper enables a specific serialization format (e.g JSON,
MessagePack, etc.) in a serialization handler, which uses Dict as the
interchanging format.
"""

from abc import ABC, abstractmethod
from typing import Dict, Union


class SerializationHelper(ABC):
    """The base class for all serialization helpers."""

    @property
    @abstractmethod
    def mime_type(self) -> str:
        """Returns the MIME type associated with the serialization format."""

    @property
    @abstractmethod
    def binary(self) -> bool:
        """Returns True if the serialization format is binary based."""

    @abstractmethod
    def from_data(self, data: Union[str, bytes]) -> Dict:
        """Deserializes a piece of data into a Dict."""

    @abstractmethod
    def to_data(self, dikt: Dict) -> Union[str, bytes]:
        """Serializes a Dict to a piece of data."""
