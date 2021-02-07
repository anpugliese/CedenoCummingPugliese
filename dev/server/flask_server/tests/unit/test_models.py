from ... import models as db_models
import pytest
import datetime

@pytest.fixture(scope='module')
def new_user():
    user = db_models.User('test_user', 'IWantToLineUp')
    return user

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that the username and password are defined correctly
    """
    assert new_user.username == 'test_user'
    assert new_user.password == 'IWantToLineUp'

@pytest.fixture(scope='module')
def new_supermarket():
    supermarket = db_models.Supermarket('Supermarket', 10, 10, 'logo')
    assert supermarket.name  == 'Supermarket'
    assert supermarket.max_capacity == 2
    return supermarket

def test_new_shopping(new_user, new_supermarket):
    current_datetime = datetime.datetime.now()
    shopping = db_models.Shopping(new_user.username, 'token', new_supermarket.name, current_datetime)
    assert shopping.enter_time == current_datetime

def test_new_waiting(new_user, new_supermarket):
    current_datetime = datetime.datetime.now()
    waiting = db_models.Waiting(new_user.username, 'token', new_supermarket.id, current_datetime, current_datetime + datetime.timedelta(days=7), 20, 1)
    assert waiting.supermarket_id == new_supermarket.id

def test_new_record(new_supermarket):
    current_datetime = datetime.datetime.now()
    record = db_models.Record(current_datetime, current_datetime+ datetime.timedelta(days=7), new_supermarket.id, 20)
    assert record.supermarket_id == new_supermarket.id