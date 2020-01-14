from abc import ABC, abstractmethod
from typing import Any

from ..misc.validation_errors import (
    ModelTypeNotMatchedError,
    RequiredFieldMissingError
)

class Field(ABC):
    """
    """
    @abstractmethod
    def get_data_type(self) -> type:
        return type(None)

    @abstractmethod
    def validate(self, v: Any, name: str = 'unnamed'):
        """
        """
        return False

class ModelMetaKls(type):
    """
    """
    def __new__(cls, clsname, superclses, attribute_dict):
        """
        """
        user_defined_fields = []
        for k in attribute_dict:
            v = attribute_dict[k]
            if issubclass(v.__class__, Field):
                user_defined_fields.append((k, v))
        fields = {}
        for (name, field) in user_defined_fields:
            # TO-DO: The following field names are reserved:
            # 'fields'
            fields[name] = field
            mask = '_' + name
            
            def fget(self):
                return getattr(self, mask)

            def fset(self, v):
                self._fields[name].validate(v)
                setattr(self, mask, v)

            def doc(self):
                return self._fields[name].description

            attribute_dict[mask] = None
            attribute_dict[name] = property(
                fget=fget,
                fset=fset,
                doc=doc
            )

        attribute_dict['_fields'] = fields
        return type.__new__(cls, clsname, superclses, attribute_dict)

class Model(metaclass=ModelMetaKls):
    """
    """
    def __init__(self, skip_validation: bool = False, **kwargs):
        """
        """
        for k in self._fields: # pylint: disable=no-member
            p = kwargs.get(k)
            mask = '_' + k
            if not p:
                required = self._fields[k].required # pylint: disable=no-member
                default = self._fields[k].default # pylint: disable=no-member
                if default:
                    p = default
                else:
                    if required:
                        raise RequiredFieldMissingError(self._fields[k], k) # pylint: disable=no-member

            if skip_validation:
                setattr(self, mask, p)
            else:
                setattr(self, k, p)
    
    @classmethod
    def get_data_type(cls):
        """
        """
        return cls

    @classmethod
    def validate(cls, v: 'Model'):
        """
        """
        if type(v) != cls:
            raise ModelTypeNotMatchedError(cls, v)

        for k in v._fields:
            field = v._fields[k]
            val = getattr(v, k)
            field.validate(val)
