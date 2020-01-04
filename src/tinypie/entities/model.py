from .fields import Field
from ..misc.field_errors import (
    RequiredFieldMissingError,
    FieldTypeNotMatchedError
)

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
            v = kwargs.get(k)
            mask = '_' + k
            if not v:
                required = self._fields[k].required
                default = self._fields[k].default
                if not default and required:
                    raise RequiredFieldMissingError(self._fields[k], k)
                else:
                    setattr(self, mask, v)
            if skip_validation:
                setattr(self, mask, v)
            else:
                setattr(k, v)
    
    @classmethod
    def get_value_type(cls) -> type:
        return cls 

    @classmethod
    def validate(cls, v: 'Model'):
        """
        """
        if type(v) != cls:
            raise FieldTypeNotMatchedError(cls, v)

        for k in v._fields:
            field = v._fields[k]
            val = getattr(v, k)
            field.validate(val)

Field.register(Model)
