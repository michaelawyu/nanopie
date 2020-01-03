import json
import typing

from ..base import SerializerAbstract
from ...entities.fields import Field
from ...entities.model import Model
from ...misc.serialization_errors import (
    UnrecognizedTypeError,
    NotAnObjectError
)

class JSONSerializer(SerializerAbstract):
    """
    """
    def to_object(self,
                  field: Field,
                  data: typing.Union[str, int, float, bool, typing.List, Model]) -> object:
        """
        """
        data_type = field.field_type

        if data_type in [str, int, float, bool]:
            return data
        
        if type(data_type) == typing._GenericAlias and data_type._name == 'List':
            i_type = data_type.__args__[0]
            return [ self.to_object(i, i_type) for i in data ]
        
        if issubclass(data_type, Model):
            d = {}
            for k in data._fields:
                k_data = getattr(data, k)
                k_type = data._fields[k]
                d[k] = self.to_object(k_data, k_type)
            return d

        raise UnrecognizedTypeError(field)

    def serialize(self, entity: Model) -> str:
        """
        """
        d = self.to_object(entity.__class__, entity)
        return json.dumps(d)

    def deserialize(self, kls: type, json_str: str) -> Model:
        """
        """
        d = json.loads(json_str)
        if type(d) is not dict:
            raise NotAnObjectError(d)

        init_params = {}
        for k in d:
            pass

        raise NotImplementedError