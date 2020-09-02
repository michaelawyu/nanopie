"""This module includes the JSON serialization helper.
"""

import json
from typing import Dict, Optional

from .base import SerializationHelper


class JSONSerializationHelper(SerializationHelper):
    """The JSON serialization helper."""

    def __init__(
        self, load_args: Optional[Dict] = None, dump_args: Optional[Dict] = None
    ):
        """Initializes a JSON serialization helper.

        Args:
            load_args (Dict, Optional): Keyword arguments for JSON
                deserialization. See
                https://docs.python.org/3/library/json.html#json.loads.
            dump_args (Dict, Optional): Keyword arguments for JSON
                serialization. See
                https://docs.python.org/3/library/json.html#json.dumps.
        """
        self._load_args = load_args if load_args else {}
        self._dump_args = dump_args if dump_args else {}

    @property
    def mime_type(self) -> str:
        """Returns the MIME type associated with the JSON format."""
        return "application/json"

    @property
    def binary(self) -> bool:
        """Returns False as JSON is not a binary format."""
        return False

    def from_data(self, data: str) -> Dict:
        """Deserializes a JSON string into a Dict."""
        return json.loads(data, **self._load_args)

    def to_data(self, dikt: Dict) -> str:
        """Serializes a Dict to a JSON string."""
        return json.dumps(dikt, **self._dump_args)
