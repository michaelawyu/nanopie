import json
from typing import Dict, Optional

from .base import SerializationHelper

class JSONSerializationHelper(SerializationHelper):
    """
    """
    def __init__(self,
                 load_args: Optional[Dict] = None,
                 dump_args: Optional[Dict] = None):
        """
        """
        self._load_args = load_args if load_args else {}
        self._dump_args = dump_args if dump_args else {}

    @property
    def mime_type(self) -> str:
        """
        """
        return 'application/json'
    
    @property
    def binary(self) -> bool:
        """
        """
        return False
    
    def from_data(self, data: str) -> Dict:
        """
        """
        return json.loads(data, **self._load_args)
    
    def to_data(self, dikt: Dict) -> str:
        """
        """
        return json.dumps(dikt, **self._dump_args)
    