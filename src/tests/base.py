import os

from flask_testing import TestCase

from src import app, db


class BaseTesting(TestCase):
    """ Base tests """

    def create_app(self):
        app.config.from_object("src.config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
