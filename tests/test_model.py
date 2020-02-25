import pytest

from nanopie import (
    StringField,
    IntField,
    FloatField,
    BoolField,
    ArrayField,
    ObjectField,
    Model
)
from nanopie.misc.errors import (
    ValidationError,
    StringMaxLengthExceededError,
    RequiredFieldMissingError,

)

def test_simple_model():
    class SimpleModel(Model):
        a = StringField()
        b = IntField()
        c = FloatField()
        d = BoolField()
        e = ArrayField(
            item_field=IntField()
        )
    
    s = SimpleModel()
    assert s.a == None
    assert s.b == None
    assert s.c == None
    assert s.d == None
    assert s.e == None

    s = SimpleModel(
        a='Test',
        b=1,
        c=1.0,
        d=True,
        e=[]
    )
    assert s.a == 'Test'
    assert s.b == 1
    assert s.c == 1.0
    assert s.d == True
    assert s.e == []

def test_simple_model_init():
    str_field = StringField(max_length=5, min_length=2)
    int_field = IntField(default=4)
    float_field = FloatField(required=True)

    class SimpleModel(Model):
        a = str_field
        b = int_field
        c = float_field
    
    with pytest.raises(StringMaxLengthExceededError) as ex:
        s = SimpleModel( # pylint: disable=unused-variable
            a='Long Message',
            b=2,
            c=1.0
        )

    assert ex.value.source == str_field
    assert ex.value.data == 'Long Message'
    assert ex.value.response == None

    s = SimpleModel(
        a = 'Test',
        c = 1.0
    )

    assert s.a == 'Test'
    assert s.b == 4
    assert s.c == 1.0

    with pytest.raises(RequiredFieldMissingError) as ex:
        s = SimpleModel(
            a = 'Test'
        )
    
    assert ex.value.source == float_field
    assert ex.value.data == None
    assert ex.value.response == None

def test_simple_model_int_skip_validation():
    class SimpleModel(Model):
        a = StringField(max_length=5, min_length=2)
        b = IntField(default=4)
        c = FloatField(required=True)
    
    s = SimpleModel(skip_validation=True)

    assert s.a == None
    assert s.b == None
    assert s.c == None

def test_model_data_type():
    class SimpleModel(Model):
        a = StringField()

    assert SimpleModel.get_data_type() == SimpleModel

def test_simple_model_to_dikt():
    class SimpleModel(Model):
        a = StringField(max_length=5, min_length=2)
        b = IntField(default=4)
        c = FloatField(required=True)
        d = BoolField(default=True)
        e = ArrayField(
            item_field=IntField(maximum=10, minimum=2),
            max_items=5,
            min_items=1
        )
    
    s = SimpleModel(
        a='Test',
        c=1.0,
        e=[2,3,4]
    )

    assert s.to_dikt() == {
        'a': 'Test',
        'b': 4,
        'c': 1.0,
        'd': True,
        'e': [2,3,4]
    }

    assert s.to_dikt(skip_validation=False) == {
        'a': 'Test',
        'b': 4,
        'c': 1.0,
        'd': True,
        'e': [2,3,4]
    }

def test_simple_model_from_dikt():
    class SimpleModel(Model):
        a = StringField(max_length=5, min_length=2)
        b = IntField(default=4)
        c = FloatField(required=True)
        d = BoolField(default=True)
        e = ArrayField(
            item_field=IntField(maximum=10, minimum=2),
            max_items=5,
            min_items=1
        )
    
    dikt = {
        'a': 'Test',
        'b': 4,
        'c': 1.0,
        'd': True,
        'e': [2,3,4]
    }

    s = SimpleModel.from_dikt(dikt)

    assert s.a == 'Test'
    assert s.b == 4
    assert s.c == 1.0
    assert s.d == True
    assert s.e == [2,3,4]

    dikt = {
        'a': 'Long Message',
        'b': 10,
        'e': [10,20,30,40,50,60]
    }

    s = SimpleModel.from_dikt(dikt)

    assert s.a == 'Long Message'
    assert s.b == 10
    assert s.c == None
    assert s.d == None
    assert s.e == [10,20,30,40,50,60]

    with pytest.raises(ValidationError) as ex:
        s = SimpleModel.from_dikt(dikt, skip_validation=False)

