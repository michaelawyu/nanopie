import json
from typing import Any, Dict, List, Optional, Union

from .base import Serializer
from ..models.base import Model
from ..misc.serialization_errors import (
    UnrecognizedTypeError,
    NoRefModelError,
    NoInputDataError
)

class JSONSerializer(Serializer):
    """
    """
    def serialize(self,
                  data: 'Model',
                  ref: 'ModelMetaKls' = None) -> str:
        """
        """
        def to_object(data: Union[str, int, float, bool, List, 'Model'],
                      ref: Union['Field', 'ModelMetaKls']):
            """
            """
            data_type = ref.get_data_type()

            if data_type in [str, int, float, bool]:
                return data
            
            if data_type == List:
                item_field = ref.item_field
                return [ to_object(item, item_field) for item in data ]

            if issubclass(data_type, Model):
                dikt = {}
                for k in data_type._fields:
                    child_data = getattr(data, k)
                    child_field = data_type._fields[k]
                    dikt[k] = to_object(child_data, child_field)
                return dikt
            
            raise UnrecognizedTypeError(source=ref)

        if ref:
            dikt = to_object(data, ref)
        elif issubclass(data.__class__, Model):
            dikt = to_object(data, data.__class__)
        else:
            raise NoRefModelError(data=data)
        
        return json.dumps(dikt)
    
    def deserialize(self,
                    data: str,
                    ref: Union['Field', 'ModelMetaKls']) -> Union[str, int, float, bool, List, 'Model']:
        """
        """
        dikt = json.loads(data)

        def from_object(data: Union[str, int, float, bool, List, Dict],
                        ref: Union['Field', 'ModelMetaKls']):
            """
            """
            data_type = ref.get_data_type()

            if data_type in [str, int, float, bool]:
                return data

            if data_type == List:
                item_field = ref.item_field
                return [ from_object(item, item_field) for item in data ]
            
            if issubclass(data_type, Model):
                instance = data_type(skip_validation=True)
                for k in data_type._fields:
                    mask = '_' + k
                    child_data = data.get(k)
                    child_field = data_type._fields[k]
                    setattr(instance, mask, from_object(child_data, child_field))
            
            raise UnrecognizedTypeError(source=ref)

        return from_object(dikt, ref)
    
    @property
    def mime_type(self):
        return 'application/json'
