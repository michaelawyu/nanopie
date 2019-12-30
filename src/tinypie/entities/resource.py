import inspect

from .fields import Field
from ..misc.errors import FieldValidationError

class ResourceMetaKls(type):
    """
    """
    def __new__(cls, clsname, superclses, attribute_dict):
        """
        """
        predicate = lambda member: True if issubclass(member, Field) else False
        user_defined_fields = inspect.getmembers(cls, predicate)
        fields = {}
        for (field_name, field_obj) in user_defined_fields:
            fields[field_name] = field_obj
            mask = '_' + field_name
            
            def fget(self):
                return getattr(self, mask)

            def fset(self, v):
                self.fields[field_name].validate(v)
                setattr(self, mask, v)

            def doc(self):
                return self.fields[field_name].description

            attribute_dict[field_name] = property(
                fget=fget,
                fset=fset,
                doc=doc
            )
        attribute_dict['_fields'] = fields
        return type.__new__(clsname, superclses, attribute_dict)

class Resource(Field, metaclass=ResourceMetaKls):
    """
    """
    def __init__(self, bypass_validation: bool = False, **kwargs):
        """
        """
        if bypass_validation:
            for k in kwargs:
                if self._fields.get(k): # pylint: disable=no-member
                    mask = '_' + k
                    setattr(self, mask, kwargs[k])
        else:
            for k in kwargs:
                if self._fields.get(k): # pylint: disable=no-member
                    setattr(self, k, kwargs[k])

    def validate(self, v):
        """
        """
        raise NotImplementedError
