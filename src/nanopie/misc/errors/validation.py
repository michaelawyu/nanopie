"""This module includes all the validation related exceptions.
"""

from typing import Any, List, Optional, Union

from .base import ValidationError
from .. import format_error_message


class ModelTypeNotMatchedError(ValidationError):
    """The validation exception for mismatched models, i.e. the input data
    is of a model type different from the one used for validation.
    """

    _message = "Input is not of the given type."

    def __init__(
        self, source: "ModelMetaCls", data: Any, message: Optional[str] = None
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message, source=source, data=data
            )

        super().__init__(message, source=source, data=data)


class RequiredFieldMissingError(ValidationError):
    """The validation exception for missing required fields."""

    _message = "A required field is missing."

    def __init__(
        self,
        source: "Field",
        assigned_field_name: Optional[str],
        message: Optional[str] = None,
    ):
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
            )

        super().__init__(message, source=source, data=None)


class FieldTypeNotMatchedError(ValidationError):
    """The validation exception for mismatched fields, i.e. the input data
    is of a data type not associated with the field used for validation.
    """

    _message = "Input is not of the given field type."

    def __init__(
        self,
        source: "Field",
        assigned_field_name: Optional[str],
        data: Any,
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class ListItemTypeNotMatchedError(ValidationError):
    """The validation exception for mismatched item fields, i.e. one or more
    items in the input array is of a data type not associated with the
    item field specified in the array field.
    """

    _message = "One or more items in the list is not of the given field type."

    def __init__(
        self,
        source: "ArrayField",
        assigned_field_name: Optional[str],
        data: Any,
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class StringMaxLengthExceededError(ValidationError):
    """The validation exception for strings that are too long."""

    _message = "Input string is too long."

    def __init__(
        self,
        source: "StringField",
        assigned_field_name: Optional[str],
        data: str,
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class StringMinLengthBelowError(ValidationError):
    """The validation exception for strings that are too short."""

    _message = "Input string is too short."

    def __init__(
        self,
        source: "StringField",
        assigned_field_name: Optional[str],
        data: str,
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class StringPatternNotMatchedError(ValidationError):
    """The validation exception for mismatched string patterns, i.e. the
    input string does not match the pattern (regular expression) specified
    in the string field.
    """

    _message = "Input string does not match the given pattern."

    def __init__(
        self,
        source: "StringField",
        assigned_field_name: Optional[str],
        data: str,
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class NumberMaxExceededError(ValidationError):
    """The validation exception for numbers that are too large."""

    _message = "Input number is too large."

    def __init__(
        self,
        source: Union["FloatField", "IntField"],
        assigned_field_name: Optional[str],
        data: Union[float, int],
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class NumberMinBelowError(ValidationError):
    """The validation exception for numbers that are too small."""

    _message = "Input number is too small."

    def __init__(
        self,
        source: Union["FloatField", "IntField"],
        assigned_field_name: Optional[str],
        data: Union[float, int],
        message: Optional[str] = None,
    ):
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class ListTooManyItemsError(ValidationError):
    """The validation exception for oversized arrays/lists."""

    _message = "Input list has too many items."

    def __init__(
        self,
        source: "ArrayField",
        assigned_field_name: Optional[str],
        data: List[Any],
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)


class ListTooLittleItemsError(ValidationError):
    """The validation exception for undersized arrays/lists."""

    _message = "Input list has too little items."

    def __init__(
        self,
        source: "ArrayField",
        assigned_field_name: Optional[str],
        data: List[Any],
        message: Optional[str] = None,
    ):
        """"""
        if not message:
            message = format_error_message(
                message=self._message,
                source=source,
                assigned_field_name=assigned_field_name,
                data=data,
            )

        super().__init__(message, source=source, data=data)
