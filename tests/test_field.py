import pytest

from nanopie import (
    StringField,
    IntField,
    FloatField,
    ArrayField,
)
from nanopie.misc.errors import (
    RequiredFieldMissingError,
    FieldTypeNotMatchedError,
    StringMaxLengthExceededError,
    StringMinLengthBelowError,
    StringPatternNotMatchedError,
    NumberMaxExceededError,
    NumberMinBelowError
)

def test_string_field_empty():
    f = StringField()

    assert f.format == None
    assert f.max_length == None
    assert f.min_length == None
    assert f.pattern == None
    assert f.required == False
    assert f.default == None
    assert f.description == ''

def test_string_field_data_type():
    f = StringField()

    assert f.get_data_type() == str

def test_string_field_validate():
    f = StringField(
        format='format',
        max_length=10,
        min_length=5,
        pattern='^He.*d!$',
        required=True,
    )

    f.validate('He ld!')

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
        f.validate('Hello World!')
    assert ex.value.source == f
    assert ex.value.data == 'Hello World!'
    assert ex.value.response == None
    
    with pytest.raises(StringMinLengthBelowError) as ex:
        f.validate('Hed!')
    assert ex.value.source == f
    assert ex.value.data == 'Hed!'
    assert ex.value.response == None
    
    with pytest.raises(StringPatternNotMatchedError) as ex:
        f.validate('Test Msg')
    assert ex.value.source == f
    assert ex.value.data == 'Test Msg'
    assert ex.value.response == None

def test_float_field_empty():
    f = FloatField()

    assert f.maximum == None
    assert f.exclusive_maximum == False
    assert f.minimum == None
    assert f.exclusive_minimum == False
    assert f.required == False
    assert f.default == None
    assert f.description == ''

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
        default=3.0
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
        f.validate('4.0')
    assert ex.value.source == f
    assert ex.value.data == '4.0'
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
        default=3.0
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
