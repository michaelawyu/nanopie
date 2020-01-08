from .fields import Field
from ..misc.model_errors import (
    ResourceParentKlsAlreadyExistsError,
    ResourceIdentifierFieldAlreadyExistsError,
    ResourceIdentifierFieldNotExists
)
from ..misc.validation_errors import (
    ModelTypeNotMatchedError,
    FieldTypeNotMatchedError,
    RequiredFieldMissingError
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

class ResourceMetaKls(ModelMetaKls):
    """
    """
    def __new__(cls, clsname, superclses, attribute_dict):
        # TO-DO: The following field names are reserved:
        # 'parent_resource_kls', 'identifier_field_name', and 'fields'
        attribute_dict['_parent_resource_kls'] = None
        attribute_dict['_identifier_field_name'] = None
        return super().__new__(cls, clsname, superclses, attribute_dict)

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
    def get_value_type(cls):
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

class Resource(Model, metaclass=ResourceMetaKls):
    """
    """
    @classmethod
    def set_parent_resource_kls(cls, resource_kls: 'ResourceMetaKls'):
        if cls._parent_resource_kls:
            raise ResourceParentKlsAlreadyExistsError(source=cls)
        
        cls._parent_resource_kls = resource_kls

    @classmethod
    def get_parent_resource_kls(cls):
        return cls._parent_resource_kls
    
    @classmethod
    def set_identifier_field_name(cls, field_name: str):
        if cls._identifier_field_name:
            raise ResourceIdentifierFieldAlreadyExistsError(source=cls,
                identifier_field_name=field_name)
        
        if not cls._fields.get(field_name): # pylint: disable=no-member
            raise ResourceIdentifierFieldNotExists(source=cls,
                identifier_field_name=field_name)

        cls._identifier_field_name = field_name
    
    @classmethod
    def get_identifier_field_name(cls):
        return cls._identifier_field_name
    