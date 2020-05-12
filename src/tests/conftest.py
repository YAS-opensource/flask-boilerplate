import pytest

from src import app, db


@pytest.fixture(scope="module")
def client():
    # setup app with test config
    app.config.from_object("src.config.TestingConfig")
    # create test client
    client = app.test_client()

    # preparing app context for the testing phase
    ctx = app.app_context()
    ctx.push()
    # tests happen here
    yield client

    ctx.pop()


@pytest.fixture(scope="module")
def database():

    # initiate database
    db.create_all()
    # commit changes
    db.session.commit()

    # tests happen here
    yield db

    # teardown
    db.session.remove()
    db.drop_all()
