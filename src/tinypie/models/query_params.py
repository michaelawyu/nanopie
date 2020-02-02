from typing import Dict, List

from .base import Field, Model, ModelMetaKls

class QueryParametersMetaKls(ModelMetaKls):
    """
    """
    def __new__(cls, clsname, superclses, attribute_dict):
        """
        """
        for k in attribute_dict:
            v = attribute_dict[k]
            if isinstance(v, Field):
                if issubclass(v.get_data_type(), Model):
                    raise ValueError('Nested objects are not allowed in query '
                                     'parameters.')
                if v.get_data_type() == List and \
                   v.item_field.get_data_type() not in [str, int, float, bool]:
                    raise ValueError('Nested objects are not allowed in query '
                                     'parameters.')

        return super().__new__(cls, clsname, superclses, attribute_dict)

class QueryParameters(Model, metaclass=QueryParametersMetaKls):
    """
    """
    @classmethod
    def parse_from_dict(cls, dikt: Dict):
        """
        """
        raise NotImplementedError

    @classmethod
    def parse_from_query_str(cls, query_str: str):
        """
        """
        raise NotImplementedError
