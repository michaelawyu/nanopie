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
    """
    """

    def __init__(
        self,
        format: Optional[str] = None,  # pylint: disable=redefined-builtin
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        pattern: Optional[int] = None,
        required: bool = False,
        default: Optional[str] = None,
        description: str = "",
    ):
        """
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
        """
        """
        return str

    def validate(self, v: Any, name: str = "unassigned_field"):
        """
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
    """
    """

    def __init__(
        self,
        maximum: Optional[float] = None,
        exclusive_maximum: bool = False,
        minimum: Optional[float] = None,
        exclusive_minimum: bool = False,
        required: bool = False,
        default: Optional[float] = None,
        description: str = "",
    ):
        """
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
        """
        """
        return float

    def validate(self, v: Any, name: str = "unassigned_field"):
        """
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
    """
    """

    def __init__(
        self,
        maximum: Optional[int] = None,
        exclusive_maximum: bool = False,
        minimum: Optional[int] = None,
        exclusive_minimum: bool = False,
        required: bool = False,
        default: Optional[int] = None,
        description: str = "",
    ):
        """
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
        """
        """
        return int

    def validate(self, v: Any, name: str = "unassigned_field"):
        """
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
    """
    """

    def __init__(
        self,
        required: bool = False,
        default: Optional[bool] = None,
        description: str = "",
    ):
        """
        """
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """
        """
        return bool

    def validate(self, v: Any, name: str = "unassigned_field"):
        """
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
    """
    """

    def __init__(
        self,
        item_field: Field,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        required: bool = False,
        default: Optional[List[Any]] = None,
        description: str = "",
    ):
        """
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
        """
        """
        return list

    def validate(self, v: List[Any], name: str = "unassigned_field"):
        """
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
    """
    """

    def __init__(
        self,
        model: "ModelMetaCls",
        required: bool = False,
        default: Optional["Model"] = None,
        description: str = "",
    ):
        """
        """
        self.model = model
        self.required = required
        self.description = description
        if default:
            self.validate(v=default)
        self.default = default

    def get_data_type(self) -> type:
        """
        """
        return self.model

    def validate(self, v: "Model", name: str = "unassigned_field"):
        """
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
