import os
import unittest

from src import app, db


class BaseTesting(unittest.TestCase):
    """ Base tests """

    client = None

    def __init__(self, methodName):
        self.client = app.test_client(self)
        super().__init__(methodName)

    def create_app(self):
        app.config.from_object("src.config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    unittest.run