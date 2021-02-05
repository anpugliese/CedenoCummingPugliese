import pytest
import json
from ... import models as db_models
from ...main import db


@pytest.fixture(scope='module')
def constants():
    # Create a test client using the Flask application configured for testing
    username = "username"
    password = "password"
    return {'username': username, 'password': password}

@pytest.fixture(scope='module')
def auth_user(test_client, constants):
    valid_json = json.dumps(constants)
    print(valid_json)

    response = test_client.post('/register', json=constants)
    assert response.status_code == 201

    response = test_client.post('/auth', json=constants)
    assert response.status_code == 200

    token = json.loads(response.data)["access_token"]
    return token


def test_supermarkets(test_client, auth_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/supermarkets_list',  headers={'Authorization': 'JWT ' + auth_user})
    json_data = json.loads(response.data)["supermarkets"]
    assert response.status_code == 200
    assert len(json_data) == 0

    sp = db_models.Supermarket("Carrefour", 0.0, 0.0, "")
    db.session.add(sp) 
    db.session.commit()

    response = test_client.get('/supermarkets_list',  headers={'Authorization': 'JWT ' + auth_user})
    json_data = json.loads(response.data)["supermarkets"]
    assert len(json_data) == 1

    