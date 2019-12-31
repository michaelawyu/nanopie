from .fields import Field
from ..misc.field_errors import RequiredFieldMissingError

class ResourceMetaKls(type):
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

            attribute_dict[mask] = None
            attribute_dict[field_name] = property(
                fget=fget,
                fset=fset,
                doc=doc
            )
        attribute_dict['_fields'] = fields
        return type.__new__(cls, clsname, superclses, attribute_dict)

class Resource(metaclass=ResourceMetaKls):
    """
    """
    def __init__(self, bypass_validation: bool = False, **kwargs):
        """
        """
        for k in self._fields: # pylint: disable=no-member
            v = kwargs.get(k)
            mask = '_' + k
            if not v:
                default_v = self._fields[k].default
                if not default_v and v.required:
                    raise RequiredFieldMissingError(self._fields[k], k)
                else:
                    setattr(self, mask, v)
            if bypass_validation:
                setattr(self, mask, v)
            else:
                setattr(k, v)
        
    @classmethod
    def field_type(cls) -> type:
        return cls 

    @classmethod
    def validate(cls, v):
        """
        """
        raise NotImplementedError

Field.register(Resource)
