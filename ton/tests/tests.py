"""All tests"""
from ton import application
from flask.ext.testing import TestCase


class StatusTest(TestCase):
    def create_app(self):
        app = application.app
        app.config['TESTING'] = True
        return app

    def test_get_index(self):
        r = self.client.get("/")
        self.assert200(r)
