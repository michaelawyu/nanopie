import json

import pytest

from nanopie.model import Model
from nanopie.fields import (
    StringField,
    IntField,
    FloatField,
    BoolField,
    ArrayField,
    ObjectField
)
from nanopie.serialization import (
    HTTPSerializationHandler,
    JSONSerializationHelper
)
from nanopie.globals import (
    request,
    parsed_request
)
from nanopie.misc.errors import SerializationError
from nanopie.handler import SimpleHandler
from nanopie.services.http.io import HTTPResponse

class SimpleModel(Model):
    str_field = StringField()
    int_field = IntField()
    float_field = FloatField()
    bool_field = BoolField()

simple_model = SimpleModel(str_field='Test Message',
                           int_field=1,
                           float_field=1.0,
                           bool_field=True)

simple_model_data = {
    'str_field': 'Test Message',
    'int_field': 1,
    'float_field': 1.0,
    'bool_field': True
}

simple_model_data_altchar = {
    'str-field': 'Test Message',
    'int-field': 1,
    'float-field': 1.0,
    'bool-field': True
}

class NestedModel(Model):
    str_field = StringField()
    int_field = IntField()
    float_field = FloatField()
    bool_field = BoolField()
    array_field = ArrayField(item_field=IntField())
    object_field = ObjectField(model=SimpleModel)

nested_model = NestedModel(str_field='Outer Test Message',
                           int_field=2,
                           float_field=2.0,
                           bool_field=False,
                           array_field=[5,10,15],
                           object_field=simple_model)

nested_model_data = {
    'str_field': 'Outer Test Message',
    'int_field': 2,
    'float_field': 2.0,
    'bool_field': False,
    'array_field': [5,10,15],
    'object_field': simple_model_data
}

@pytest.fixture
def http_serialization_handler_json():
    return HTTPSerializationHandler(
        headers_cls=SimpleModel,
        query_args_cls=SimpleModel,
        data_cls=NestedModel,
        serialization_helper=JSONSerializationHelper()
    )

def test_http_serialization_handler_json(
    setup_ctx, http_serialization_handler_json):
    request.mime_type = http_serialization_handler_json._serialization_helper.mime_type # pylint: disable=assigning-non-slot
    request.headers = simple_model_data_altchar # pylint: disable=assigning-non-slot
    request.query_args = simple_model_data # pylint: disable=assigning-non-slot
    request.text_data = json.dumps(nested_model_data) # pylint: disable=assigning-non-slot

    assert http_serialization_handler_json() == None
    assert parsed_request.headers.str_field == 'Test Message'
    assert parsed_request.headers.int_field == 1
    assert parsed_request.headers.float_field == 1.0
    assert parsed_request.headers.bool_field == True
    assert parsed_request.query_args.str_field == 'Test Message'
    assert parsed_request.query_args.int_field == 1
    assert parsed_request.query_args.float_field == 1.0
    assert parsed_request.query_args.bool_field == True
    assert parsed_request.data.str_field == 'Outer Test Message'
    assert parsed_request.data.int_field == 2
    assert parsed_request.data.float_field == 2.0
    assert parsed_request.data.array_field == [5,10,15]
    assert parsed_request.data.object_field.str_field == 'Test Message'
    assert parsed_request.data.object_field.int_field == 1
    assert parsed_request.data.object_field.float_field == 1.0
    assert parsed_request.data.object_field.bool_field == True

def test_http_serialization_handler_json_failure_not_HTTP_request_mime_type(
    setup_ctx, http_serialization_handler_json):
    with pytest.raises(AttributeError) as ex:
        http_serialization_handler_json()

    assert 'not a valid HTTP request' in str(ex.value)

def test_http_serialization_handler_json_failure_not_HTTP_request_headers(
    setup_ctx, http_serialization_handler_json):
    request.mime_type = '' # pylint: disable=assigning-non-slot

    with pytest.raises(AttributeError) as ex:
        http_serialization_handler_json()
    
    assert 'not a valid HTTP request' in str(ex.value)

def test_http_serialization_handler_json_failure_not_HTTP_request_query_args(
    setup_ctx, http_serialization_handler_json):
    request.mime_type = '' # pylint: disable=assigning-non-slot
    request.headers = {} # pylint: disable=assigning-non-slot

    with pytest.raises(AttributeError) as ex:
        http_serialization_handler_json()

    assert 'not a valid HTTP request' in str(ex.value)

def test_http_serialization_handler_json_failure_not_HTTP_request_data(
    setup_ctx, http_serialization_handler_json):
    request.mime_type = '' # pylint: disable=assigning-non-slot
    request.headers = {} # pylint: disable=assigning-non-slot
    request.query_args = {} # pylint: disable=assigning-non-slot

    with pytest.raises(AttributeError) as ex:
        http_serialization_handler_json()
    
    assert 'not a valid HTTP request' in str(ex.value)

def test_http_serialization_handler_json_failure_mismatched_mime_type(
    setup_ctx, http_serialization_handler_json):
    request.mime_type = 'text/html' # pylint: disable=assigning-non-slot
    request.headers = {} # pylint: disable=assigning-non-slot
    request.query_args = {} # pylint: disable=assigning-non-slot
    request.text_data = '' # pylint: disable=assigning-non-slot

    with pytest.raises(SerializationError) as ex:
        http_serialization_handler_json()
    
    assert 'does not have the expected mime type' in str(ex.value)
    assert ex.value.response.status_code == 400
    assert ex.value.response.headers == {}
    assert ex.value.response.mime_type == 'text/html'
    assert '400 Bad Request' in ex.value.response.data

def test_http_serialization_handler_json_response_parsing(
    setup_ctx, http_serialization_handler_json):
    def response_func(*args, **kwargs):
        return HTTPResponse(status_code=200,
                            headers=simple_model,
                            data=nested_model)
    
    simple_handler = SimpleHandler(func=response_func)
    http_serialization_handler_json.wraps(simple_handler)

    request.mime_type = http_serialization_handler_json._serialization_helper.mime_type # pylint: disable=assigning-non-slot
    request.headers = simple_model_data_altchar # pylint: disable=assigning-non-slot
    request.query_args = simple_model_data # pylint: disable=assigning-non-slot
    request.text_data = json.dumps(nested_model_data) # pylint: disable=assigning-non-slot

    res = http_serialization_handler_json()
    assert isinstance(res, HTTPResponse)
    assert res.status_code == 200
    assert res.mime_type == 'application/json'
    assert res.headers == simple_model_data
    assert res.data == json.dumps(nested_model_data)

def test_http_serialization_handler_json_failure_headers_parsing(
    setup_ctx, http_serialization_handler_json):
    def response_func(*args, **kwargs):
        malformed_simple_model = SimpleModel(skip_validation=True,
                                             str_field=object(),
                                             int_field=object(),
                                             float_field=object(),
                                             bool_field=object())
        return HTTPResponse(status_code=200,
                            headers=malformed_simple_model,
                            data=nested_model)
    
    simple_handler = SimpleHandler(func=response_func)
    http_serialization_handler_json.wraps(simple_handler)

    request.mime_type = http_serialization_handler_json._serialization_helper.mime_type # pylint: disable=assigning-non-slot
    request.headers = simple_model_data_altchar # pylint: disable=assigning-non-slot
    request.query_args = simple_model_data # pylint: disable=assigning-non-slot
    request.text_data = json.dumps(nested_model_data) # pylint: disable=assigning-non-slot

    with pytest.raises(SerializationError) as ex:
        http_serialization_handler_json()
    
    assert 'Cannot serialize the headers' in str(ex.value)
                        
def test_http_serialization_handler_json_failure_payload_parsing(
    setup_ctx, http_serialization_handler_json):
    def response_func(*args, **kwargs):
        malformed_nested_model = NestedModel(skip_validation=True,
                                             str_field=object(),
                                             int_field=object(),
                                             float_field=object(),
                                             bool_field=object(),
                                             array_field=object(),
                                             object_field=object())
        return HTTPResponse(status_code=200,
                            headers=simple_model,
                            data=malformed_nested_model)
    
    simple_handler = SimpleHandler(func=response_func)
    http_serialization_handler_json.wraps(simple_handler)

    request.mime_type = http_serialization_handler_json._serialization_helper.mime_type # pylint: disable=assigning-non-slot
    request.headers = simple_model_data_altchar # pylint: disable=assigning-non-slot
    request.query_args = simple_model_data # pylint: disable=assigning-non-slot
    request.text_data = json.dumps(nested_model_data) # pylint: disable=assigning-non-slot

    with pytest.raises(SerializationError) as ex:
        http_serialization_handler_json()
    
    assert 'Cannot serialize the data' in str(ex.value)
