import json

import pytest

from .simple_app import app, dummy_storage

@pytest.fixture
def test_client():
    app.testing = True
    return app.test_client()

def test_get_user(test_client):
    user_data_to_get = dummy_storage[0]
    uid = user_data_to_get.get("uid")

    res = test_client.get('/users/{}'.format(uid), follow_redirects=True)
    assert res.status_code == 200

    user_data = res.json    
    assert user_data == user_data_to_get


def test_create_user(test_client):
    user_data_to_create = {
        "first_name": "Jane",
        "last_name": "Doe",
        "age": 24
    }
    data = json.dumps(user_data_to_create)

    res = test_client.post('/users', data=data, follow_redirects=True)
    assert res.status_code == 200

    user_data = res.json
    assert user_data['first_name'] == 'Jane'
    assert user_data['last_name'] == 'Doe'
    assert user_data['age'] == 24


def test_update_user(test_client):
    pass


def test_delete_user(test_client):
    pass


def test_list_users(test_client):
    pass
