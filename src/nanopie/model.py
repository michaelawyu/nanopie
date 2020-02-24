from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Dict, List, Union

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
            mask = "_" + name

            def fget(self, mask):
                return getattr(self, mask)

            def fset(self, name, mask, v):
                self._fields[name].validate(v)
                setattr(self, mask, v)

            def doc(self, name):
                return self._fields[name].description

            attribute_dict[mask] = None
            attribute_dict[name] = property(
                fget=partial(fget, mask=mask),
                fset=partial(fset, name=name, mask=mask),
                doc=partial(doc, name=name),
            )

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
            p = kwargs.get(k)
            mask = "_" + k
            if not p:
                required = self._fields[k].required  # pylint: disable=no-member
                default = self._fields[k].default  # pylint: disable=no-member
                if default:
                    p = default
                else:
                    if required:
                        raise RequiredFieldMissingError(
                            self._fields[k], k # pylint: disable=no-member
                        )

            if skip_validation:
                setattr(self, mask, p)
            else:
                setattr(self, k, p)

    def to_dikt(self):
        """
        """

        def helper(data: Union[str, int, float, bool, List, "Model"], ref: "Field"):
            """
            """
            data_type = ref.get_data_type()

            if data_type in [str, int, float, bool] and type(data) == data_type:
                return data
            elif data_type == List and type(data) == list:
                item_field = ref.item_field
                return [helper(item, item_field) for item in data]
            elif issubclass(data_type, Model) and issubclass(data, Model):
                return data.to_dikt()
            else:
                message = format_error_message(
                    message="Unsupported data type.", data=data, ref=ref
                )
                raise RuntimeError(message)

        dikt = {}
        for k in self._fields:  # pylint: disable=no-member
            field = self._fields[k]  # pylint: disable=no-member
            v = helper(getattr(self, k), field)
            dikt[k] = v

        return dikt

    @classmethod
    def from_dikt(cls, dikt: Dict):
        """
        """

        def helper(data: Union[str, int, float, bool, List, "Model"], ref: "Field"):
            """
            """
            data_type = ref.get_data_type()

            if data_type in [str, int, float, bool] and type(data) == data_type:
                return data
            elif data_type == List and type(data) == list:
                item_field = ref.item_field
                return [helper(item, item_field) for item in data]
            elif issubclass(data_type, Model) and type(data) == dict:
                return data_type.from_dikt(data)
            else:
                message = format_error_message(
                    message="Unsupported data type.", data=data, ref=ref
                )
                raise RuntimeError(message)

        obj = cls(skip_validation=True)
        for k in cls._fields:  # pylint: disable=no-member
            field = cls._fields[k]  # pylint: disable=no-member
            v = helper(dikt[k], field)
            setattr(obj, k, v)

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
