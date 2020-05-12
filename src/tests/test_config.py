import os
from src import app, db


def test_testingConfig():
    """TestingConfig test."""

    app.config.from_object("src.config.TestingConfig")

    assert not app.config["SECRET_KEY"] is None
    assert app.config["DEBUG"] == True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///unittest_db.db"


def test_devConfig():
    """DevConfig test."""

    app.config.from_object("src.config.DevConfig")

    assert not (app.config["SECRET_KEY"] is None)
    assert app.config["DEBUG"] == True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv(
        "DATABASE_URL", "sqlite:///test.db"
    )


def test_productionConfig():
    """ProductionConfig test."""

    app.config.from_object("src.config.ProductionConfig")

    assert not (app.config["SECRET_KEY"] is None)
    assert app.config["DEBUG"] == False
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL")
    assert not (app.config["SQLALCHEMY_DATABASE_URI"] is None)
