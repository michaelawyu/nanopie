import json
from typing import Dict

from .base import SerializationHelper

class JSONSerializationHelper(SerializationHelper):
    """
    """
    def __init__(self, load_args: Dict = {}, dump_args: Dict = {}):
        """
        """
        self._load_args = load_args
        self._dump_args = dump_args

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
    