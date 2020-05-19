import json

import pytest

from nanopie.serialization.helpers import JSONSerializationHelper

dikt = {"test": "message"}
data = json.dumps(dikt)


@pytest.fixture
def json_serialization_helper():
    return JSONSerializationHelper()


def test_json_serialization_helper_mime_type(json_serialization_helper):
    assert json_serialization_helper.mime_type == "application/json"


def test_json_serialization_helper_binary(json_serialization_helper):
    assert json_serialization_helper.binary == False


def test_json_serialization_helper_to_data(json_serialization_helper):
    assert json_serialization_helper.to_data(dikt) == data


def test_json_serialization_helper_from_data(json_serialization_helper):
    assert json_serialization_helper.from_data(data) == dikt
