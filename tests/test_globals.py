from functools import partial

import pytest

from nanopie.globals import (
    look_up_attr,
    look_up_item,
    svc_ctx,
    parsed_request,
    svc,
    endpoint,
    request,
)


class Object(object):
    pass


def test_look_up_attr():
    obj = Object()
    obj.attr = 0

    assert look_up_attr(ctx=obj, name="attr") == 0


def test_look_up_attr_none():
    obj = Object()

    with pytest.raises(RuntimeError) as ex:
        look_up_attr(ctx=obj, name="attr")
    assert "No context is available" in str(ex.value)


def test_look_up_item():
    dikt = {"item": 0}

    assert look_up_item(dikt=dikt, name="item") == 0


def test_look_up_item_none():
    dikt = {}

    with pytest.raises(RuntimeError) as ex:
        look_up_item(dikt=dikt, name="item")
    assert "Specified object is not available yet." in str(ex.value)


def test_svc_ctx(setup_ctx):
    assert svc_ctx.get("parsed_request") != None
    assert svc_ctx.get("svc") != None
    assert svc_ctx.get("endpoint") != None
    assert svc_ctx.get("request") != None


def test_parsed_request(setup_ctx):
    assert parsed_request._extract_mock_name() == "parsed_request"


def test_svc(setup_ctx):
    assert svc._extract_mock_name() == "svc"


def test_endpoint(setup_ctx):
    assert endpoint._extract_mock_name() == "endpoint"


def test_request(setup_ctx):
    assert request._extract_mock_name() == "request"
