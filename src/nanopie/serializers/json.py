import json
from typing import Any, Dict, List, Optional, Union

from .base import Serializer
from ..models.base import Model
from ..misc.errors import (
    UnrecognizedTypeError,
    NoRefModelError,
    NoInputDataError
)

class JSONSerializer(Serializer):
    """
    """
    def serialize(self,
                  data: 'Model') -> str:
        """
        """
        return json.dumps(data.to_object())
    
    def deserialize(self,
                    data: str,
                    ref: 'ModelMetaKls') -> 'Model':
        """
        """
        dikt = json.loads(data)

        return ref.from_dikt(dikt)
    
    @property
    def mime_type(self):
        return 'application/json'
