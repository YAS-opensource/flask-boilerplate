import os
import unittest

from flask_testing import TestCase

from src import app, db


class TestingConfigTest(TestCase):
    """ TestingConfig test """

    def create_app(self):
        app.config.from_object("src.config.TestingConfig")
        return app

    def test_config_vars(self):
        self.assertFalse(app.config["SECRET_KEY"] is None)
        self.assertTrue(app.config["DEBUG"] == True)
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///unittest_db.db"
        )


class DevConfigTest(TestCase):
    """ DevConfig test """

    def create_app(self):
        app.config.from_object("src.config.DevConfig")
        return app

    def test_config_vars(self):
        self.assertFalse(app.config["SECRET_KEY"] is None)
        self.assertTrue(app.config["DEBUG"] == True)
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"]
            == os.getenv("DATABASE_URL", "sqlite:///test.db")
        )


class ProductionConfigTest(TestCase):
    """ ProductionConfig test """

    def create_app(self):
        app.config.from_object("src.config.ProductionConfig")
        return app

    def test_config_vars(self):
        self.assertFalse(app.config["SECRET_KEY"] is None)
        self.assertTrue(app.config["DEBUG"] == False)
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL")
        )


if __name__ == ("__main__"):
    unittest.main()
