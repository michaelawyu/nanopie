import json
from typing import Any, Dict, List, Union

from ..base import SerializerAbstract
from ...entities.model import Model
from ...misc.serialization_errors import (
    UnrecognizedTypeError,
    NotAnObjectError
)

class JSONSerializer(SerializerAbstract):
    """
    """
    def serialize(self,
                  value: Union[str, int, float, bool, List, Model],
                  field: Optional[Union['Field', 'ModelMetaKls']] = None) -> str:
        """
        """
        def to_object(value: Union[str, int, float, bool, List, Model],
                      field: Union['Field', 'ModelMetaKls']):
            """
            """
            value_type = field.get_value_type()

            if value_type in [str, int, float, bool]:
                return value
            
            if value_type == List:
                item_field = field.item_field
                return [ to_object(item, item_field) for item in value ]

            if issubclass(value_type, Model):
                dikt = {}
                for k in value_type._fields:
                    child_value = getattr(value, k)
                    child_field = value_type._fields[k]
                    dikt[k] = to_object(child_value, child_field)
                return dikt
            
            raise UnrecognizedTypeError(field)
        
        if not field:
            dikt = to_object(value, value.__class__)
        else:
            dikt = to_object(value, field)
        
        return json.dumps(dikt)
    
    def deserialize(self,
                    value_str: str,
                    field: Union['Field', 'ModelMetaKls']) -> Union[str, int, float, bool, List, Model]:
        """
        """
        value = json.loads(value_str)

        def from_object(value: object,
                        field: Union['Field', 'ModelMetaKls']):
            """
            """
            value_type = field.get_value_type()

            if value_type in [str, int, float, bool]:
                return value
            
            if value_type == List:
                item_field = field.item_field
                return [ from_object(item, item_field) for item in value ]
            
            if issubclass(value_type, Model):
                instance = value_type(skip_validation=True)
                for k in value_type._fields:
                    mask = '_' + k
                    child_value = value.get(k)
                    child_field = value_type._fields[k]
                    setattr(instance, mask, from_object(child_value, child_field))
            
            raise UnrecognizedTypeError(field)

        return from_object(value, field)
