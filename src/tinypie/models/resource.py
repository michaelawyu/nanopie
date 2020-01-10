from .base import Model, ModelMetaKls
from ..misc.model_errors import (
    ResourceParentKlsAlreadyExistsError,
    ResourceIdentifierFieldAlreadyExistsError,
    ResourceIdentifierFieldNotExists
)

class ResourceMetaKls(ModelMetaKls):
    """
    """
    def __new__(cls, clsname, superclses, attribute_dict):
        # TO-DO: The following field names are reserved:
        # 'parent_resource_kls', 'identifier_field_name', and 'fields'
        attribute_dict['_parent_resource_kls'] = None
        attribute_dict['_identifier_field_name'] = None
        return super().__new__(cls, clsname, superclses, attribute_dict)

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