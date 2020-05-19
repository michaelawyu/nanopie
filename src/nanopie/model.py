from abc import ABC, abstractmethod
from functools import partialmethod
from typing import Any, Dict, List, Optional, Union

from .misc import format_error_message
from .misc.errors import ModelTypeNotMatchedError, RequiredFieldMissingError


class Field(ABC):
    """
    """

    @abstractmethod
    def get_data_type(self) -> type:
        """
        """

    @abstractmethod
    def validate(self, v: Any, name: str = "unassigned_field"):
        """
        """


class ModelMetaCls(type):
    """
    """

    def __new__(cls, clsname, superclses, attribute_dict):
        """
        """

        class PropertyDescriptor:
            """
            """

            __slots__ = ("name", "mask")

            def __init__(self, name: str, mask: str):
                """
                """
                self.name = name
                self.mask = mask

            def __get__(self, obj, type=None) -> Any:
                """
                """
                return getattr(obj, self.mask)

            def __set__(self, obj, value):
                """
                """
                obj._fields[self.name].validate(value, name)
                setattr(obj, self.mask, value)

        user_defined_fields = []
        for k in attribute_dict:
            v = attribute_dict[k]
            if issubclass(v.__class__, Field):
                user_defined_fields.append((k, v))

        fields = {}
        for (name, field) in user_defined_fields:
            fields[name] = field
            mask = "_" + name

            descriptor = PropertyDescriptor(name=name, mask=mask)

            attribute_dict[mask] = None
            attribute_dict[name] = descriptor

        attribute_dict["_fields"] = fields
        attribute_dict["_extras"] = {}
        return type.__new__(cls, clsname, superclses, attribute_dict)


class Model(metaclass=ModelMetaCls):
    """
    """

    __slots__ = ()

    def __init__(self, skip_validation: bool = False, **kwargs):
        """
        """
        for k in self._fields:  # pylint: disable=no-member
            mask = "_" + k
            p = kwargs.get(k)

            if skip_validation:
                setattr(self, mask, p)
                continue

            if p == None:
                required = self._fields[k].required  # pylint: disable=no-member
                default = self._fields[k].default  # pylint: disable=no-member
                if default:
                    setattr(self, mask, default)
                    continue
                else:
                    if required:
                        raise RequiredFieldMissingError(
                            self._fields[k], k  # pylint: disable=no-member
                        )

            setattr(self, k, p)

    def to_dikt(self, altchar: Optional[str] = None, skip_validation: bool = True):
        """
        """
        if not skip_validation:
            self.validate(v=self)

        def helper(data: Union[str, int, float, bool, List, "Model"]):
            """
            """
            if type(data) in [str, int, float, bool]:
                return data
            elif type(data) == list:
                return [helper(item) for item in data]
            elif isinstance(data, Model):
                return data.to_dikt(skip_validation=skip_validation)
            else:
                message = "The data is of an unsupported type."
                message = format_error_message(message=message, data=data)
                raise RuntimeError(message)

        dikt = {}
        for k in self._fields:  # pylint: disable=no-member
            v = helper(getattr(self, k))
            if altchar:
                k = k.replace("_", altchar[0])
            dikt[k] = v

        return dikt

    @classmethod
    def from_dikt(
        cls,
        dikt: Dict,
        altchar: Optional[str] = None,
        skip_validation: bool = True,
        type_cast: bool = False,
    ):
        """
        """

        def helper(data: Union[str, int, float, bool, List, "Model"], ref: "Field"):
            """
            """
            data_type = ref.get_data_type()

            if data_type in [str, int, float, bool]:
                if type_cast:
                    try:
                        data = data_type(data)
                    except:
                        pass
                return data
            elif data_type == list and type(data) != list:
                return data
            elif data_type == list and type(data) == list:
                item_field = ref.item_field
                return [helper(item, item_field) for item in data]
            elif issubclass(data_type, Model) and type(data) != dict:
                return data
            elif issubclass(data_type, Model) and type(data) == dict:
                return data_type.from_dikt(data)
            else:
                message = (
                    "The data is not of the type specified in the field"
                    ", or the field specifies an unsupported type."
                )
                message = format_error_message(message=message, data=data, ref=ref)
                raise RuntimeError(message)

        obj = cls(skip_validation=True)
        for k in cls._fields:  # pylint: disable=no-member
            mask = "_" + k
            field = cls._fields[k]  # pylint: disable=no-member
            if altchar:
                k = k.replace("_", altchar[0])
            v = helper(dikt.get(k), field)
            setattr(obj, mask, v)

        if not skip_validation:
            cls.validate(v=obj)

        return obj

    @classmethod
    def get_data_type(cls):
        """
        """
        return cls

    @classmethod
    def validate(cls, v: "Model"):
        """
        """
        if type(v) != cls:
            raise ModelTypeNotMatchedError(cls, v)

        for k in v._fields:
            field = v._fields[k]
            val = getattr(v, k)
            field.validate(v=val, name=k)
