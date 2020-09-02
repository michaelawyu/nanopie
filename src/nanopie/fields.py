"""This module includes the fields nanopie provides for modeling data.

Each field has a number of restraints, which developers can specify to
easily validate data. Many of these restraints come from the OpenAPI 3
specification.

See also `model.py`.
"""

import re
from typing import Any, List, Optional

from .model import Field, Model
from .misc.errors import (
    FieldTypeNotMatchedError,
    ListItemTypeNotMatchedError,
    ListTooManyItemsError,
    ListTooLittleItemsError,
    NumberMaxExceededError,
    NumberMinBelowError,
    RequiredFieldMissingError,
    StringMaxLengthExceededError,
    StringMinLengthBelowError,
    StringPatternNotMatchedError,
)


class StringField(Field):
    """A field for string typed data."""

    def __init__(
        self,
        format: Optional[str] = None,  # pylint: disable=redefined-builtin
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        pattern: Optional[str] = None,
        required: bool = False,
        default: Optional[str] = None,
        description: str = "A string field",
    ):
        """Initializes the field.

        Args:
            format (str, Optional): The format of this field, e.g. byte or
                binary. This restraint is for notation purposes only; nanopie
                does not validate data against the specified format.
            max_length (int, Optional): The maximum length of this field.
            min_length (int, Optional): The minimum length of this field.
            pattern (str, Optional): The pattern of this field, in the form
                of a regular expression, e.g. `^[a-z]*$` (any lower case
                alphabetic string)
            required (bool): If set to True, this field is required in a model,
                e.g. it cannot be `None` (an empty string, however, is still
                valid).
            default (str, Optional): The default value of this field.
            description (str): The description of this field.
        """
        self.format = format  # pylint: disable=redefined-builtin
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """Returns the data type associated with this field (str)."""
        return str

    def validate(self, v: Any, name: str = "unassigned_field"):
        """Validates a piece of data against this field.

        Args:
            v (Any): a piece of data.
            name (str): The name of the field in a model (if any).
        """
        if type(v) != str:
            if v == None:
                if self.required:
                    raise RequiredFieldMissingError(
                        source=self, assigned_field_name=name
                    )
                else:
                    return
            else:
                raise FieldTypeNotMatchedError(
                    source=self, assigned_field_name=name, data=v
                )

        if self.max_length and len(v) > self.max_length:
            raise StringMaxLengthExceededError(
                source=self, assigned_field_name=name, data=v
            )

        if self.min_length and len(v) < self.min_length:
            raise StringMinLengthBelowError(
                source=self, assigned_field_name=name, data=v
            )

        if self.pattern and not re.match(self.pattern, v):
            raise StringPatternNotMatchedError(
                source=self, assigned_field_name=name, data=v
            )


class FloatField(Field):
    """A field of float typed data."""

    def __init__(
        self,
        maximum: Optional[float] = None,
        exclusive_maximum: bool = False,
        minimum: Optional[float] = None,
        exclusive_minimum: bool = False,
        required: bool = False,
        default: Optional[float] = None,
        description: str = "A float field",
    ):
        """Initializes the field.

        Args:
            maximum (float, Optional): The maximum value of this field.
            exclusive_maximum (bool): If set to True, the boundary maximum
                value will be excluded (`>` instead of `>=`).
            minimum (float, Optional): The minimum value of this field.
            exclusive_minimum (bool): If set to True, the boundary minimum
                value will be exclused (`<` instead `<=`).
            required (bool): If set to True, this field is required in a model,
                e.g. it cannot be `None`.
            default (float, Optional): The default value of this field.
            description (str): The description of this field.
        """
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """Returns the data type associated with this field (float)."""
        return float

    def validate(self, v: Any, name: str = "unassigned_field"):
        """Validates a piece of data against this field.

        Args:
            v (Any): a piece of data.
            name (str): The name of the field in a model (if any).
        """
        if type(v) != float:
            if v == None:
                if self.required:
                    raise RequiredFieldMissingError(
                        source=self, assigned_field_name=name
                    )
                else:
                    return
            else:
                raise FieldTypeNotMatchedError(
                    source=self, assigned_field_name=name, data=v
                )

        if self.maximum and v >= self.maximum:
            if v == self.maximum and not self.exclusive_maximum:
                pass
            else:
                raise NumberMaxExceededError(
                    source=self, assigned_field_name=name, data=v
                )

        if self.minimum and v <= self.minimum:
            if v == self.minimum and not self.exclusive_minimum:
                pass
            else:
                raise NumberMinBelowError(source=self, assigned_field_name=name, data=v)


class IntField(Field):
    """A field of int typed data."""

    def __init__(
        self,
        maximum: Optional[int] = None,
        exclusive_maximum: bool = False,
        minimum: Optional[int] = None,
        exclusive_minimum: bool = False,
        required: bool = False,
        default: Optional[int] = None,
        description: str = "An int field",
    ):
        """Initializes the field.

        Args:
            maximum (float, Optional): The maximum value of this field.
            exclusive_maximum (bool): If set to True, the boundary maximum
                value will be excluded (`>` instead of `>=`).
            minimum (float, Optional): The minimum value of this field.
            exclusive_minimum (bool): If set to True, the boundary minimum
                value will be exclused (`<` instead `<=`).
            required (bool): If set to True, this field is required in a model,
                e.g. it cannot be `None`.
            default (float, Optional): The default value of this field.
            description (str): The description of this field.
        """
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """Returns the data type associated with this field (int)."""
        return int

    def validate(self, v: Any, name: str = "unassigned_field"):
        """Validates a piece of data against this field.

        Args:
            v (Any): a piece of data.
            name (str): The name of the field in a model (if any).
        """
        if type(v) != int:
            if v == None:
                if self.required:
                    raise RequiredFieldMissingError(
                        source=self, assigned_field_name=name
                    )
                else:
                    return
            else:
                raise FieldTypeNotMatchedError(
                    source=self, assigned_field_name=name, data=v
                )

        if self.maximum and v >= self.maximum:
            if v == self.maximum and not self.exclusive_maximum:
                pass
            else:
                raise NumberMaxExceededError(
                    source=self, assigned_field_name=name, data=v
                )

        if self.minimum and v <= self.minimum:
            if v == self.minimum and not self.exclusive_minimum:
                pass
            else:
                raise NumberMinBelowError(source=self, assigned_field_name=name, data=v)


class BoolField(Field):
    """A field of bool typed data."""

    def __init__(
        self,
        required: bool = False,
        default: Optional[bool] = None,
        description: str = "A bool field",
    ):
        """Initializes the field.

        Args:
            required (bool): If set to True, this field is required in a model,
                e.g. it cannot be `None`.
            default (bool, Optional): The default value of this field.
            description (str): The description of this field.
        """
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """Returns the data type associated with this field (bool)."""
        return bool

    def validate(self, v: Any, name: str = "unassigned_field"):
        """Validates a piece of data against this field.

        Args:
            v (Any): a piece of data.
            name (str): The name of the field in a model (if any).
        """
        if type(v) != bool:
            if v == None:
                if self.required:
                    raise RequiredFieldMissingError(
                        source=self, assigned_field_name=name
                    )
                else:
                    return
            else:
                raise FieldTypeNotMatchedError(
                    source=self, assigned_field_name=name, data=v
                )


class ArrayField(Field):
    """A field of array/list typed data."""

    def __init__(
        self,
        item_field: Field,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        required: bool = False,
        default: Optional[List[Any]] = None,
        description: str = "An array field",
    ):
        """Initializes the field.

        Args:
            item_field (Field): A field that describes the items in the array.
            min_items (int, Optional): The minimum number of items in the array.
            max_items (int, Optional): The maximum number of items in the array.
            required (bool): If set to True, this field is required in a model,
                e.g. it cannot be `None`.
            default (List[Any], Optional): The default value of this field.
            description (str): The description of this field.
        """
        self.item_field = item_field
        self.min_items = min_items
        self.max_items = max_items
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """Returns the data type associated with this field (list)."""
        return list

    def validate(self, v: List[Any], name: str = "unassigned_field"):
        """Validates a piece of data against this field.

        Args:
            v (Any): a piece of data.
            name (str): The name of the field in a model (if any).
        """
        if type(v) != list:
            if v == None:
                if self.required:
                    raise RequiredFieldMissingError(
                        source=self, assigned_field_name=name
                    )
                else:
                    return
            else:
                raise FieldTypeNotMatchedError(
                    source=self, assigned_field_name=name, data=v
                )

        if self.min_items and len(v) < self.min_items:
            raise ListTooLittleItemsError(source=self, assigned_field_name=name, data=v)

        if self.max_items and len(v) > self.max_items:
            raise ListTooManyItemsError(source=self, assigned_field_name=name, data=v)

        for item in v:
            if type(item) != self.item_field.get_data_type():
                raise ListItemTypeNotMatchedError(
                    source=self, assigned_field_name=name, data=v
                )
            self.item_field.validate(item)


class ObjectField(Field):
    """A field of object typed data."""

    def __init__(
        self,
        model: "ModelMetaCls",
        required: bool = False,
        default: Optional["Model"] = None,
        description: str = "An object field",
    ):
        """Initializes the field.

        Args:
            model (ModelMetaCls): A model that describes the object.
            required (bool): If set to True, this field is required in a model,
                e.g. it cannot be `None`.
            default (Model, Optional): The default value of this field.
            description (str): The description of this field.
        """
        self.model = model
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """Returns the data type associated with this field (a subclass of Model)."""
        return self.model

    def validate(self, v: "Model", name: str = "unassigned_field"):
        """Validates a piece of data against this field.

        Args:
            v (Any): a piece of data.
            name (str): The name of the field in a model (if any).
        """
        if not issubclass(v.__class__, self.model):
            if v == None:
                if self.required:
                    raise RequiredFieldMissingError(
                        source=self, assigned_field_name=name
                    )
                else:
                    return
            else:
                raise FieldTypeNotMatchedError(
                    source=self, assigned_field_name=name, data=v
                )

        for k in self.model._fields:
            child_field = self.model._fields[k]
            child_field_value = getattr(v, k)
            child_field.validate(child_field_value, k)
