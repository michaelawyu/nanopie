import pytest

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
    StringMaxLengthExceededError,
    RequiredFieldMissingError,
    NumberMaxExceededError,
)


class SimpleModel(Model):
    a = StringField()
    b = IntField()
    c = FloatField()
    d = BoolField()
    e = ArrayField(item_field=IntField())


class SimpleModelWithRestraints(Model):
    a = StringField(max_length=5, min_length=2)
    b = IntField(maximum=10, minimum=1, default=4)
    c = FloatField(maximum=10.0, minimum=1.0, required=True)
    d = BoolField(default=True)
    e = ArrayField(item_field=IntField(maximum=10, minimum=2), max_items=5, min_items=1)


class NestedModel(Model):
    a = ArrayField(item_field=IntField(maximum=10, minimum=1))
    b = ArrayField(item_field=ArrayField(item_field=IntField(maximum=10, minimum=1)))
    c = ObjectField(model=SimpleModelWithRestraints)


def test_simple_model():
    s = SimpleModel()
    assert s.a == None
    assert s.b == None
    assert s.c == None
    assert s.d == None
    assert s.e == None


def test_simple_model_init():
    s = SimpleModel(a="Test", b=1, c=1.0, d=True, e=[2, 3])
    assert s.a == "Test"
    assert s.b == 1
    assert s.c == 1.0
    assert s.d == True
    assert s.e == [2, 3]

    with pytest.raises(StringMaxLengthExceededError) as ex:
        s = SimpleModelWithRestraints(  # pylint: disable=unused-variable
            a="Long Message", c=1.0
        )

    assert isinstance(ex.value.source, StringField)
    assert ex.value.data == "Long Message"
    assert ex.value.response == None

    s = SimpleModelWithRestraints(a="Test", c=1.0)

    assert s.a == "Test"
    assert s.b == 4
    assert s.c == 1.0
    assert s.d == True
    assert s.e == None

    with pytest.raises(RequiredFieldMissingError) as ex:
        s = SimpleModelWithRestraints(a="Test")

    assert isinstance(ex.value.source, FloatField)
    assert ex.value.data == None
    assert ex.value.response == None


def test_simple_model_init_skip_validation():
    s = SimpleModelWithRestraints(skip_validation=True)

    assert s.a == None
    assert s.b == None
    assert s.c == None
    assert s.d == None
    assert s.e == None


def test_model_data_type():
    assert SimpleModel.get_data_type() == SimpleModel
    assert SimpleModelWithRestraints.get_data_type() == SimpleModelWithRestraints


def test_simple_model_to_dikt():
    s = SimpleModelWithRestraints(a="Test", c=1.0, e=[2, 3, 4])

    assert s.to_dikt() == {"a": "Test", "b": 4, "c": 1.0, "d": True, "e": [2, 3, 4]}

    assert s.to_dikt(skip_validation=False) == {
        "a": "Test",
        "b": 4,
        "c": 1.0,
        "d": True,
        "e": [2, 3, 4],
    }


def test_simple_model_from_dikt():
    dikt = {"a": "Test", "b": 4, "c": 1.0, "d": True, "e": [2, 3, 4]}

    s = SimpleModelWithRestraints.from_dikt(dikt)

    assert s.a == "Test"
    assert s.b == 4
    assert s.c == 1.0
    assert s.d == True
    assert s.e == [2, 3, 4]

    dikt = {"a": "Long Message", "b": 10, "e": [10, 20, 30, 40, 50, 60]}

    s = SimpleModelWithRestraints.from_dikt(dikt)

    assert s.a == "Long Message"
    assert s.b == 10
    assert s.c == None
    assert s.d == True
    assert s.e == [10, 20, 30, 40, 50, 60]

    with pytest.raises(ValidationError) as ex:
        s = SimpleModelWithRestraints.from_dikt(dikt, skip_validation=False)


def test_nested_model():
    n = NestedModel()

    assert n.a == None
    assert n.b == None
    assert n.c == None


def test_nested_model_init():
    s = SimpleModelWithRestraints(a="Test", b=1, c=1.0, d=True, e=[2, 3])

    n = NestedModel(a=[2, 3, 4], b=[[2, 3, 4]], c=s)

    assert n.a == [2, 3, 4]
    assert n.b == [[2, 3, 4]]
    assert isinstance(n.c, SimpleModelWithRestraints)
    assert n.c.a == "Test"  # pylint: disable=no-member
    assert n.c.b == 1  # pylint: disable=no-member
    assert n.c.c == 1.0  # pylint: disable=no-member
    assert n.c.d == True  # pylint: disable=no-member
    assert n.c.e == [2, 3]  # pylint: disable=no-member

    with pytest.raises(NumberMaxExceededError) as ex:
        n = NestedModel(a=[1, 2, 3], b=[[2, 3, 15]], c=s)
    assert isinstance(ex.value.source, IntField)
    assert ex.value.data == 15
    assert ex.value.response == None

    with pytest.raises(NumberMaxExceededError) as ex:
        setattr(s, "_b", 15)
        n = NestedModel(a=[1, 2, 3], b=[[2, 3, 4]], c=s)
    assert isinstance(ex.value.source, IntField)
    assert ex.value.data == 15
    assert ex.value.response == None

    setattr(s, "_b", 1)


def test_nested_model_to_dikt():
    s = SimpleModelWithRestraints(a="Test", b=1, c=1.0, d=True, e=[2, 3])

    n = NestedModel(a=[2, 3, 4], b=[[2, 3, 4], [1, 2, 3]], c=s)

    assert n.to_dikt() == {
        "a": [2, 3, 4],
        "b": [[2, 3, 4], [1, 2, 3]],
        "c": {"a": "Test", "b": 1, "c": 1.0, "d": True, "e": [2, 3]},
    }

    assert n.to_dikt(skip_validation=False) == {
        "a": [2, 3, 4],
        "b": [[2, 3, 4], [1, 2, 3]],
        "c": {"a": "Test", "b": 1, "c": 1.0, "d": True, "e": [2, 3]},
    }


def test_nested_model_from_dikt():
    dikt = {
        "a": [2, 3, 4],
        "b": [[2, 3, 4], [1, 2, 3]],
        "c": {"a": "Test", "b": 1, "c": 1.0, "d": True, "e": [2, 3]},
    }

    n = NestedModel.from_dikt(dikt)

    assert n.a == [2, 3, 4]
    assert n.b == [[2, 3, 4], [1, 2, 3]]
    assert isinstance(n.c, SimpleModelWithRestraints)
    assert n.c.a == "Test"  # pylint: disable=no-member
    assert n.c.b == 1  # pylint: disable=no-member
    assert n.c.c == 1.0  # pylint: disable=no-member
    assert n.c.d == True  # pylint: disable=no-member
    assert n.c.e == [2, 3]  # pylint: disable=no-member

    dikt["b"] = [[2, 3, 15]]

    with pytest.raises(NumberMaxExceededError) as ex:
        n = NestedModel.from_dikt(dikt, skip_validation=False)
    assert isinstance(ex.value.source, IntField)
    assert ex.value.data == 15
    assert ex.value.response == None
