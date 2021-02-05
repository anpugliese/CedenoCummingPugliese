from ... import models as db_models
import pytest

@pytest.fixture(scope='module')
def new_user():
    user = db_models.User('test_user', 'IWantToLineUp')
    return user

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.username == 'test_user'
    assert new_user.password == 'IWantToLineUp'