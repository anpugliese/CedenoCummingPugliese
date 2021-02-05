import pytest
from ..main import create_app, db

@pytest.fixture(scope='session')
def app():
    app = create_app(testing=True)
    with app.app_context():   
        # alternative pattern to app.app_context().push()
        # all commands indented under 'with' are run in the app context 
        try:
            db.create_all()
            db.session.commit()
            yield app   # Note that we changed return for yield, see below for why
        except Exception as ex:
            print("asdf")
            print(ex)
    
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='session')
def test_client(app):
    with app.test_client() as client:
        yield client