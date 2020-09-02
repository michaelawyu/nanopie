import json
import socket

import pytest

if __package__ == None or __package__ == "":
    from constants import ES256_TOKEN  # pylint: disable=no-name-in-module
    from simple_app_handlers import app, dummy_storage  # pylint: disable=import-error
else:
    from .constants import ES256_TOKEN
    from .simple_app_individual_handlers import app, dummy_storage


@pytest.fixture
def test_client():
    app.testing = True
    return app.test_client()


def test_get_user(capfd, test_client):
    user_data_to_get = dummy_storage[0]
    uid = user_data_to_get.get("uid")

    res = test_client.get(
        "/users/{}".format(uid),
        headers={"Authorization": "Bearer {}".format(ES256_TOKEN)},
        follow_redirects=True,
    )
    assert res.status_code == 200

    out, err = capfd.readouterr()
    tracing_span = json.loads(out)
    assert "Entering span get_user_logging." in err
    assert "Exiting span get_user_logging." in err
    assert tracing_span["name"] == "get_user_tracing"


def test_create_user(capfd, test_client):
    user_data_to_create = {"first_name": "Jane", "last_name": "Doe", "age": 24}
    data = json.dumps(user_data_to_create)

    res = test_client.post(
        "/users",
        headers={"Authorization": "Bearer {}".format(ES256_TOKEN)},
        data=data,
        follow_redirects=True,
    )
    assert res.status_code == 200

    user_data = res.json
    assert user_data["first_name"] == "Jane"
    assert user_data["last_name"] == "Doe"
    assert user_data["age"] == 24

    out, err = capfd.readouterr()
    tracing_span = json.loads(out)
    assert "Entering span create_user_logging." in err
    assert "Exiting span create_user_logging." in err
    assert tracing_span["name"] == "create_user_tracing"


def test_update_user(capfd, test_client):
    old_user_data = dummy_storage[0]
    uid = old_user_data.get("uid")
    user_data_to_update = {"age": 36}
    masks = ["age"]
    data = json.dumps({"user": user_data_to_update, "masks": masks})

    res = test_client.patch(
        "/users/{}?api_key=123".format(uid),
        data=data,
        follow_redirects=True,
    )
    assert res.status_code == 200

    user_data = res.json
    assert user_data["age"] == 36

    out, err = capfd.readouterr()
    tracing_span = json.loads(out)
    assert "Entering span update_user_logging." in err
    assert "Exiting span update_user_logging." in err
    assert tracing_span["name"] == "update_user_tracing"


def test_delete_user(capfd, test_client):
    user_data = dummy_storage[0]
    uid = user_data.get("uid")

    res = test_client.delete(
        "/users/{}?api_key=123".format(uid),
        follow_redirects=True,
    )
    assert res.status_code == 200

    deleted_user_data = res.json
    assert deleted_user_data == user_data

    out, err = capfd.readouterr()
    tracing_span = json.loads(out)
    assert "Entering span delete_user_logging." in err
    assert "Exiting span delete_user_logging." in err
    assert tracing_span["name"] == "delete_user_tracing"


def test_list_updates(capfd, test_client):
    user_data = dummy_storage[0]

    res = test_client.get(
        "/users",
        headers={"Authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l"},
        follow_redirects=True,
    )
    assert res.status_code == 200

    listed_users = res.json
    assert len(listed_users) == 1
    assert listed_users[0] == user_data

    out, err = capfd.readouterr()
    tracing_span = json.loads(out)
    assert "Entering span list_users_logging." in err
    assert "Exiting span list_users_logging." in err
    assert tracing_span["name"] == "list_users_tracing"


def test_verify_user(capfd, test_client):
    user_data = dummy_storage[0]
    uid = user_data.get("uid")

    res = test_client.get(
        "/users/{}:verify".format(uid),
        headers={
            "Authorization": "Basic YWxhZGRpbjpvcGVuc2VzYW1l",
            "test": "A test",
            "another_test": 4,
        },
        follow_redirects=True,
    )
    assert res.status_code == 200

    verified_user_data = res.json
    assert verified_user_data == user_data

    out, err = capfd.readouterr()
    tracing_span = json.loads(out)
    assert "Entering span verify_user_logging." in err
    assert "Exiting span verify_user_logging." in err
    assert tracing_span["name"] == "verify_user_tracing"
