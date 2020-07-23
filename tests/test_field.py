import pytest
from typing import List

from nanopie import (
    StringField,
    IntField,
    FloatField,
    BoolField,
    ArrayField,
    ObjectField,
    Model,
)
from nanopie.misc.errors import (
    ValidationError,
    RequiredFieldMissingError,
    FieldTypeNotMatchedError,
    StringMaxLengthExceededError,
    StringMinLengthBelowError,
    StringPatternNotMatchedError,
    NumberMaxExceededError,
    NumberMinBelowError,
    ListItemTypeNotMatchedError,
    ListTooLittleItemsError,
    ListTooManyItemsError,
)


def test_string_field_empty():
    f = StringField()

    assert f.format == None
    assert f.max_length == None
    assert f.min_length == None
    assert f.pattern == None
    assert f.required == False
    assert f.default == None
    assert f.description == "A string field"


def test_string_field_data_type():
    f = StringField()

    assert f.get_data_type() == str


def test_string_field_validate():
    f = StringField(
        format="format", max_length=10, min_length=5, pattern="^He.*d!$", required=True,
    )

    f.validate("He ld!")

    with pytest.raises(RequiredFieldMissingError) as ex:
        f.validate(None)
    assert ex.value.source == f
    assert ex.value.data == None
    assert ex.value.response == None

    with pytest.raises(FieldTypeNotMatchedError) as ex:
        f.validate(1)
    assert ex.value.source == f
    assert ex.value.data == 1
    assert ex.value.response == None

    with pytest.raises(StringMaxLengthExceededError) as ex:
        f.validate("Hello World!")
    assert ex.value.source == f
    assert ex.value.data == "Hello World!"
    assert ex.value.response == None

    with pytest.raises(StringMinLengthBelowError) as ex:
        f.validate("Hed!")
    assert ex.value.source == f
    assert ex.value.data == "Hed!"
    assert ex.value.response == None

    with pytest.raises(StringPatternNotMatchedError) as ex:
        f.validate("Test Msg")
    assert ex.value.source == f
    assert ex.value.data == "Test Msg"
    assert ex.value.response == None


def test_float_field_empty():
    f = FloatField()

    assert f.maximum == None
    assert f.exclusive_maximum == False
    assert f.minimum == None
    assert f.exclusive_minimum == False
    assert f.required == False
    assert f.default == None
    assert f.description == "A float field"


def test_float_field_data_type():
    f = FloatField()

    assert f.get_data_type() == float


def test_float_field_validate():
    f = FloatField(
        maximum=10.0,
        exclusive_maximum=False,
        minimum=2.0,
        exclusive_minimum=False,
        required=True,
        default=3.0,
    )

    f.validate(4.0)
    f.validate(10.0)
    f.validate(2.0)

    with pytest.raises(RequiredFieldMissingError) as ex:
        f.validate(None)
    assert ex.value.source == f
    assert ex.value.data == None
    assert ex.value.response == None

    with pytest.raises(FieldTypeNotMatchedError) as ex:
        f.validate("4.0")
    assert ex.value.source == f
    assert ex.value.data == "4.0"
    assert ex.value.response == None

    with pytest.raises(NumberMaxExceededError) as ex:
        f.validate(11.0)
    assert ex.value.source == f
    assert ex.value.data == 11.0
    assert ex.value.response == None

    with pytest.raises(NumberMinBelowError) as ex:
        f.validate(1.0)
    assert ex.value.source == f
    assert ex.value.data == 1.0
    assert ex.value.response == None


def test_float_field_validate_exclusive():
    f = FloatField(
        maximum=10.0,
        exclusive_maximum=True,
        minimum=2.0,
        exclusive_minimum=True,
        required=True,
        default=3.0,
    )

    f.validate(4.0)

    with pytest.raises(NumberMaxExceededError) as ex:
        f.validate(10.0)
    assert ex.value.source == f
    assert ex.value.data == 10.0
    assert ex.value.response == None

    with pytest.raises(NumberMinBelowError) as ex:
        f.validate(2.0)
    assert ex.value.source == f
    assert ex.value.data == 2.0
    assert ex.value.response == None


def test_int_field_empty():
    f = IntField()

    assert f.maximum == None
    assert f.exclusive_maximum == False
    assert f.minimum == None
    assert f.exclusive_minimum == False
    assert f.required == False
    assert f.default == None
    assert f.description == "An int field"


def test_int_field_data_type():
    f = IntField()

    assert f.get_data_type() == int


def test_int_field_validate():
    f = IntField(
        maximum=10,
        exclusive_maximum=False,
        minimum=2,
        exclusive_minimum=False,
        required=True,
        default=3,
    )

    f.validate(4)
    f.validate(10)
    f.validate(2)

    with pytest.raises(RequiredFieldMissingError) as ex:
        f.validate(None)
    assert ex.value.source == f
    assert ex.value.data == None
    assert ex.value.response == None

    with pytest.raises(FieldTypeNotMatchedError) as ex:
        f.validate(4.0)
    assert ex.value.source == f
    assert ex.value.data == 4.0
    assert ex.value.response == None

    with pytest.raises(NumberMaxExceededError) as ex:
        f.validate(11)
    assert ex.value.source == f
    assert ex.value.data == 11
    assert ex.value.response == None

    with pytest.raises(NumberMinBelowError) as ex:
        f.validate(1)
    assert ex.value.source == f
    assert ex.value.data == 1
    assert ex.value.response == None


def test_int_field_validate_exclusive():
    f = IntField(
        maximum=10,
        exclusive_maximum=True,
        minimum=2,
        exclusive_minimum=True,
        required=True,
        default=3,
    )

    f.validate(4)

    with pytest.raises(NumberMaxExceededError) as ex:
        f.validate(10)
    assert ex.value.source == f
    assert ex.value.data == 10
    assert ex.value.response == None

    with pytest.raises(NumberMinBelowError) as ex:
        f.validate(2)
    assert ex.value.source == f
    assert ex.value.data == 2
    assert ex.value.response == None


def test_bool_field_empty():
    f = BoolField()

    assert f.required == False
    assert f.default == None
    assert f.description == "A bool field"


def test_bool_field_data_type():
    f = BoolField()

    assert f.get_data_type() == bool


def test_bool_field_validate():
    f = BoolField(required=True, default=False)

    f.validate(True)

    with pytest.raises(RequiredFieldMissingError) as ex:
        f.validate(None)
    assert ex.value.source == f
    assert ex.value.data == None
    assert ex.value.response == None

    with pytest.raises(FieldTypeNotMatchedError) as ex:
        f.validate("")
    assert ex.value.source == f
    assert ex.value.data == ""
    assert ex.value.response == None


def test_array_field_empty():
    i = IntField()
    f = ArrayField(item_field=i)

    assert f.item_field == i
    assert f.min_items == None
    assert f.max_items == None
    assert f.required == False
    assert f.default == None
    assert f.description == "An array field"


def test_array_field_data_type():
    i = IntField()
    f = ArrayField(item_field=i)

    assert f.get_data_type() == list


def test_array_field_validate():
    i = IntField(maximum=10, minimum=2, required=True,)
    f = ArrayField(item_field=i, min_items=2, max_items=5, required=True)

    f.validate([2, 3, 4])

    with pytest.raises(RequiredFieldMissingError) as ex:
        f.validate(None)

    assert ex.value.source == f
    assert ex.value.data == None
    assert ex.value.response == None

    with pytest.raises(FieldTypeNotMatchedError) as ex:
        f.validate(1)

    assert ex.value.source == f
    assert ex.value.data == 1
    assert ex.value.response == None

    with pytest.raises(NumberMaxExceededError) as ex:
        f.validate([2, 3, 11])

    assert ex.value.source == i
    assert ex.value.data == 11
    assert ex.value.response == None

    with pytest.raises(ListItemTypeNotMatchedError) as ex:
        f.validate([2, 3, "11"])

    assert ex.value.source == f
    assert ex.value.data == [2, 3, "11"]
    assert ex.value.response == None

    with pytest.raises(ListTooManyItemsError) as ex:
        f.validate([2, 3, 4, 5, 6, 7])

    assert ex.value.source == f
    assert ex.value.data == [2, 3, 4, 5, 6, 7]
    assert ex.value.response == None

    with pytest.raises(ListTooLittleItemsError) as ex:
        f.validate([2])

    assert ex.value.source == f
    assert ex.value.data == [2]
    assert ex.value.response == None


class SimpleModel(Model):
    a = StringField(max_length=5, min_length=1)
    b = IntField(maximum=10, minimum=1, default=5)
    c = FloatField(maximum=10.0, minimum=1.0)
    d = BoolField(required=True)
    e = ArrayField(item_field=IntField(), max_items=5, min_items=1, default=[1, 2, 3])


def test_object_field():
    f = ObjectField(model=SimpleModel)

    assert f.model == SimpleModel
    assert f.required == False
    assert f.description == "An object field"
    assert f.default == None


def test_object_field_data_type():
    f = ObjectField(model=SimpleModel)

    assert f.get_data_type() == SimpleModel


def test_object_field_validate():
    f = ObjectField(model=SimpleModel, required=True)

    m = SimpleModel(a="Test", c=2.0, d=False)

    f.validate(m)

    with pytest.raises(RequiredFieldMissingError) as ex:
        f.validate(None)
    assert ex.value.source == f
    assert ex.value.data == None
    assert ex.value.response == None

    with pytest.raises(FieldTypeNotMatchedError) as ex:
        f.validate(1)
    assert ex.value.source == f
    assert ex.value.data == 1
    assert ex.value.response == None

    setattr(m, "_a", "Long Message")

    with pytest.raises(ValidationError) as ex:
        f.validate(m)
    assert isinstance(ex.value.source, StringField)
    assert ex.value.data == "Long Message"
    assert ex.value.response == None
