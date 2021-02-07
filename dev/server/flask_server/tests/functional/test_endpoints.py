import pytest
import json
from ... import models as db_models
from ...main import db

def credentials_factory(username, password):
    return {"username": username, "password": password}

@pytest.fixture(scope='module')
def user_tokens(test_client):
    user_amount = 3
    tokens = []
    for i in range(user_amount):
        user = credentials_factory("user" + str(i), "password")
        print(user)
        response = test_client.post('/register', json=user)

        response = test_client.post('/auth', json=user)
        obj={"token": json.loads(response.data)["access_token"], "username": user.get('username')}
        tokens.append(obj)
        assert response.status_code == 200

    print(tokens)
    return tokens


def test_supermarkets(test_client, user_tokens):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    auth_user = user_tokens[0].get('token')
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

def test_rejected_getin(test_client, user_tokens):
    """
    GIVEN user 1 and user 2 lining up
    WHEN user 2 tries to enter. The '/getin' page is requested (POST)
    THEN It should be rejected because it is not his turn
    """
    db.session.query(db_models.Shopping).delete()
    db.session.query(db_models.Waiting).delete()
    db.session.query(db_models.Record).delete()
    #db_models.Shopping.query.delete()
    #db_models.Waiting.query.delete()
    #db_models.Record.query.delete()
    db.session.commit()

    auth_user1 = user_tokens[0].get('token')
    user1 = user_tokens[0].get('username')
    supermarket_id = db_models.Supermarket.query.all()[0].id
    print(supermarket_id)
    body = {"username": user1, "supermarket_id":  supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user1}, json=body)
    assert response.status_code == 201

    auth_user2 = user_tokens[1].get('token')
    user2 = user_tokens[1].get('username')
    body = {"username": user2, "supermarket_id": supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 201

    body = {"token": user2}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 401

def test_accepted_getin(test_client, user_tokens):
    """
    GIVEN user 1 and user 2 lining up
    WHEN user 1 tries to enter the '/getin' page is requested (POST)
    THEN It should be accepted because it is his turn
    """
    db.session.query(db_models.Shopping).delete()
    db.session.query(db_models.Waiting).delete()
    db.session.query(db_models.Record).delete()
    db.session.commit()

    auth_user1 = user_tokens[0].get('token')
    user1 = user_tokens[0].get('username')
    supermarket_id = db_models.Supermarket.query.all()[0].id
    print(supermarket_id)
    body = {"username": user1, "supermarket_id":  supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user1}, json=body)
    assert response.status_code == 201

    auth_user2 = user_tokens[1].get('token')
    user2 = user_tokens[1].get('username')
    body = {"username": user2, "supermarket_id": supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 201

    body = {"token": user1}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user1}, json=body)
    assert response.status_code == 201

    db_models.Shopping.query.delete()
    db_models.Waiting.query.delete()
    db.session.commit()

def test_full_supermarket(test_client, user_tokens):
    """
    GIVEN user 1 and user 2 in the supermarket and user 3 lining up
    WHEN user 3 tries to enter the '/getin' page is requested (POST)
    THEN It should not be accepted because the supermarket is full
    """
    db.session.query(db_models.Shopping).delete()
    db.session.query(db_models.Waiting).delete()
    db.session.query(db_models.Record).delete()
    db.session.commit()

    auth_user1 = user_tokens[0].get('token')
    user1 = user_tokens[0].get('username')
    supermarket_id = db_models.Supermarket.query.all()[0].id
    print(supermarket_id)
    body = {"username": user1, "supermarket_id":  supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user1}, json=body)
    assert response.status_code == 201

    auth_user2 = user_tokens[1].get('token')
    user2 = user_tokens[1].get('username')
    body = {"username": user2, "supermarket_id": supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 201

    auth_user3 = user_tokens[2].get('token')
    user3 = user_tokens[2].get('username')
    body = {"username": user3, "supermarket_id": supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user3}, json=body)
    assert response.status_code == 201

    body = {"token": user1}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user1}, json=body)
    assert response.status_code == 201

    body = {"token": user2}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 201
    
    body = {"token": user3}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user3}, json=body)
    assert response.status_code == 400

    db_models.Shopping.query.delete()
    db_models.Waiting.query.delete()
    db.session.commit()


def test_now_available(test_client, user_tokens):
    """
    GIVEN user 1 and user 2 in the supermarket and user 3 lining up
    WHEN user 1 or user 2 gets out and user 3 tries to enter the '/getin' page is requested (POST)
    THEN It should be accepted because the supermarket is not full anymore
    """
    db.session.query(db_models.Shopping).delete()
    db.session.query(db_models.Waiting).delete()
    db.session.query(db_models.Record).delete()
    db.session.commit()

    auth_user1 = user_tokens[0].get('token')
    user1 = user_tokens[0].get('username')
    supermarket_id = db_models.Supermarket.query.all()[0].id
    print(supermarket_id)
    body = {"username": user1, "supermarket_id":  supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user1}, json=body)
    assert response.status_code == 201

    auth_user2 = user_tokens[1].get('token')
    user2 = user_tokens[1].get('username')
    body = {"username": user2, "supermarket_id": supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 201

    auth_user3 = user_tokens[2].get('token')
    user3 = user_tokens[2].get('username')
    body = {"username": user3, "supermarket_id": supermarket_id}
    response = test_client.post('/lineup',  headers={'Authorization': 'JWT ' + auth_user3}, json=body)
    assert response.status_code == 201

    body = {"token": user1}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user1}, json=body)
    assert response.status_code == 201

    body = {"token": user2}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 201

    body = {"token": user2}
    response = test_client.post('/getout',  headers={'Authorization': 'JWT ' + auth_user2}, json=body)
    assert response.status_code == 201
    
    body = {"token": user3}
    response = test_client.post('/getin',  headers={'Authorization': 'JWT ' + auth_user3}, json=body)
    assert response.status_code == 201

    db_models.Shopping.query.delete()
    db_models.Waiting.query.delete()
    db.session.commit()