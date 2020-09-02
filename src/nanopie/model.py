"""This module includes the base classes nanopie provides for modeling data.

In nanopie, a class that subclasses the `nanopie.Model` class becomes
a single, definite source of information (a model) about a piece of data
that nanopie can recognize. Each `nanopie.Model` objects (models) may include
a number of fields, which are pre-defined instances of the `nanopie.Field`
class that specifies the attributes of the model.

For example, a `User` model with two string attribute
(`first_name`, `last_name`) and an int attribute (`age`) looks like this
with nanopie:

```python
from nanopie import Model, StringField, IntField

class User(Model):
    first_name = StringField()
    last_name = StringField()
    age = IntField()
```

Fields and models allow developers to access and manipule a piece of
data idiomatically. One can also validate data using its model. When
you specify a microservice/API service with nanopie using models as inputs
and outputs, nanopie can also use them to serialize and deserialize data
for you automatically.

```python
user = User(first_name="John", last_name="Smith", age=34)
print(user.first_name)
print(user.last_name)
print(user.age)

# Serialize and deserialize data
user_dikt = user.to_dikt()
user = user.from_dikt(user_dikt)

# Validate data
user.age = "invalid_age_string"
user.validate() # Will raise an exception
```
"""

from abc import ABC, abstractmethod
from functools import partialmethod
import distutils
from typing import Any, Dict, List, Optional, Union

from .misc import format_error_message
from .misc.errors import ModelTypeNotMatchedError, RequiredFieldMissingError


class Field(ABC):
    """The base class for all fields.

    See `fields.py` for a list of supported fields in nanopie.
    """

    @abstractmethod
    def get_data_type(self) -> type:
        """Gets the type of data associated with this field."""

    @abstractmethod
    def validate(self, v: Any, name: str = "unassigned_field"):
        """Validates a piece of data using this field.

        Args:
            v (Any): An object.
            name (str): The name of the field in a model (if any).
        """


class ModelMetaCls(type):
    """The metaclass for the Model class."""

    def __new__(cls, clsname, superclses, attribute_dict):
        """Overides the __new__ magic method of the class.

        The overriden method reads the class definition that user provides
        and set the class up as a `Model`. It collects all the specified
        fields, saves them in the `_fields` private attribute, and
        configures them as properties with getter and setter.
        """

        class PropertyDescriptor:
            """The descriptor class for setting up fields as properties."""

            __slots__ = ("name", "mask")

            def __init__(self, name: str, mask: str):
                """Initializes the descriptor.

                Args:
                    name (str): The name of the field.
                    mask (str): The name of the (private) attribute that
                        associates with the property.
                """
                self.name = name
                self.mask = mask

            def __get__(self, obj, type=None) -> Any:
                """The getter method of the property."""
                return getattr(obj, self.mask)

            def __set__(self, obj, value):
                """The setter method of the property."""
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
    """The base class for all models."""

    __slots__ = ()

    def __init__(self, skip_validation: bool = False, **kwargs):
        """Initializes a model instance.

        Args:
            skip_validation (bool): If set to True, the initializer will not
                validate the provided values for each field.
            **kwargs: Values for each field.
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
                if default != None:
                    setattr(self, mask, default)
                    continue
                else:
                    if required:
                        raise RequiredFieldMissingError(
                            self._fields[k], k  # pylint: disable=no-member
                        )

            setattr(self, k, p)

    def to_dikt(
        self, altchar: Optional[str] = None, skip_validation: bool = True
    ) -> Dict:
        """Parses the model instance into a Dict.

        The name of each field will become a key and the value of each field
        will become the value associated with the key.

        Args:
            altchar (str): A character that this method will use to replace
                the `_` character in the names of the fields.
            skip_validation (bool): If set to True, this method will not
                validate the model instance before parsing.

        Returns:
            dict: a Dict parsed from the model instance.
        """
        if not skip_validation:
            self.validate()

        def helper(data: Union[str, int, float, bool, List, "Model"]):
            """A helper method for serializing fields and their values."""
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
        case_insensitive: bool = False,
        skip_validation: bool = True,
        type_cast: bool = False,
        use_default: bool = True,
    ) -> "Model":
        """Parses a Dict into a model instance.

        This method will match the keys of the Dict with the names of the
        fields specified in the model. If a match is found, the value
        associated with key will be assigned to the matching field in the
        created model instance.

        Args:
            dikt (Dict): the Dict to parse.
            altchar (str): A character the this method will use to replace
                the `_` character in the names of the fields.
            case_insensitive (bool): If set to True, this method will ignore
                cases when matching the keys with the names of the fields.
            skip_validation (bool): If set to True, this method will not
                validate the created model instance after parsing.
            type_cast (bool): If set to True, this method will perform a
                type cast when a match is found between the keys of the Dict
                and the names of the fields but the value of the associated
                key is not of the data type associated with the field. The type
                case fails quietly if unsuccessful.
            use_default (bool): If set to True, this method will assign to
                each fields that cannot be matched the default value (if any)
                asscoiated with them.

        Returns:
            Model: A model instance parsed from the Dict.
        """

        def helper(data: Union[str, int, float, bool, List, "Model"], ref: "Field"):
            """"""
            data_type = ref.get_data_type()

            if data_type in [str, int, float, bool]:
                if type_cast:
                    try:
                        if data_type != bool:
                            data = data_type(data)
                        else:
                            data = distutils.util.strtobool(data)
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
            if case_insensitive:
                ks = list(dikt.keys())
                ks_mapping = {}
                for it in ks:
                    ks_mapping[it.lower()] = it
                true_k = ks_mapping.get(k.lower())
                v = helper(dikt.get(true_k), field)
            else:
                v = helper(dikt.get(k), field)
            if v == None and use_default and field.default != None:
                setattr(obj, mask, field.default)
            else:
                setattr(obj, mask, v)

        if not skip_validation:
            cls.validate_instance(v=obj)

        return obj

    @classmethod
    def get_data_type(cls) -> "Model":
        """Gets the type of data associated with this model (which is itself).

        Returns:
            Model: the model itself.
        """
        return cls

    @classmethod
    def validate_instance(cls, v: "Model"):
        """Validates a piece of data using this model.

        Args:
            v (Model): a model instance.
        """
        if type(v) != cls:
            raise ModelTypeNotMatchedError(cls, v)

        for k in v._fields:
            field = v._fields[k]
            val = getattr(v, k)
            field.validate(v=val, name=k)

    def validate(self):
        """Validates the model instance itself."""
        self.__class__.validate_instance(self)
