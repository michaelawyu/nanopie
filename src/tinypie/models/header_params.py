from typing import Dict, List

from .base import Field, Model, ModelMetaKls
from ..misc.model_errors import NoNestedObjectInHeaderParametersError

def get_http_header_name_alias(var_name: str) -> str:
    """
    """
    raise NotImplementedError

class HeaderParametersMetaKls(ModelMetaKls):
    """
    """
    def __new__(cls, clsname, superclses, attribute_dict):
        """
        """
        field_aliases = {}
        for k in attribute_dict:
            v = attribute_dict[k]
            if isinstance(v, Field):
                if issubclass(v.get_data_type(), Model):
                    raise NoNestedObjectInHeaderParametersError(source=cls)
                if v.get_data_type() == List and \
                   v.item_field.get_data_type() not in [str, int, float, bool]:
                    raise NoNestedObjectInHeaderParametersError(source=cls)
                k_alias = get_http_header_name_alias(k)
                field_aliases[k] = k_alias

        attribute_dict['_field_aliases'] = field_aliases
        return super().__new__(cls, clsname, super, attribute_dict)

class HeaderParameters(Model, metaclass=HeaderParametersMetaKls):
    """
    """
    @classmethod
    def parse_from_dict(cls, headers: Dict):
        """
        """
        raise NotImplementedError
