import json
import socket

import pytest

if __package__ == None or __package__ == "":
    from constants import ES256_TOKEN  # pylint: disable=no-name-in-module
    from simple_app_handlers import app, dummy_storage  # pylint: disable=import-error
else:
    from .constants import ES256_TOKEN
    from .simple_app_handlers import app, dummy_storage


@pytest.fixture
def test_client():
    app.testing = True
    return app.test_client()


def verify_outerr(capfd):
    out, err = capfd.readouterr()
    tracing_span = json.loads(out)

    assert "Entering span unspecified_span." in err
    assert "Exiting span unspecified_span." in err
    assert tracing_span["name"] == "unspecified"


def test_get_user(capfd, test_client):
    user_data_to_get = dummy_storage[0]
    uid = user_data_to_get.get("uid")

    res = test_client.get(
        "/users/{}".format(uid),
        headers={"Authorization": "Bearer {}".format(ES256_TOKEN)},
        follow_redirects=True,
    )
    assert res.status_code == 200

    verify_outerr(capfd)


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

    verify_outerr(capfd)


def test_update_user(capfd, test_client):
    old_user_data = dummy_storage[0]
    uid = old_user_data.get("uid")
    user_data_to_update = {"age": 36}
    masks = ["age"]
    data = json.dumps({"user": user_data_to_update, "masks": masks})

    res = test_client.patch(
        "/users/{}".format(uid),
        headers={"Authorization": "Bearer {}".format(ES256_TOKEN)},
        data=data,
        follow_redirects=True,
    )
    assert res.status_code == 200

    user_data = res.json
    assert user_data["age"] == 36

    verify_outerr(capfd)


def test_delete_user(capfd, test_client):
    user_data = dummy_storage[0]
    uid = user_data.get("uid")

    res = test_client.delete(
        "/users/{}".format(uid),
        headers={"Authorization": "Bearer {}".format(ES256_TOKEN)},
        follow_redirects=True,
    )
    assert res.status_code == 200

    deleted_user_data = res.json
    assert deleted_user_data == user_data

    verify_outerr(capfd)


def test_list_users(capfd, test_client):
    user_data = dummy_storage[0]

    res = test_client.get(
        "/users",
        headers={"Authorization": "Bearer {}".format(ES256_TOKEN)},
        follow_redirects=True,
    )
    assert res.status_code == 200

    listed_users = res.json
    assert len(listed_users) == 1
    assert listed_users[0] == user_data

    verify_outerr(capfd)


def test_verify_user(capfd, test_client):
    user_data = dummy_storage[0]
    uid = user_data.get("uid")

    res = test_client.get(
        "/users/{}:verify".format(uid),
        headers={"Authorization": "Bearer {}".format(ES256_TOKEN)},
        follow_redirects=True,
    )
    assert res.status_code == 200

    verified_user_data = res.json
    assert verified_user_data == user_data

    verify_outerr(capfd)
