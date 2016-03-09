"""All tests"""
import os

from ton import application
from ton.models import db
from flask.ext.testing import TestCase
from flask import url_for


class StatusTest(TestCase):
    def setUp(self):
        _cwd = os.path.realpath(os.path.dirname(__file__))
        project_root = os.path.dirname(_cwd)  # Go up one dir
        self.db_uri = 'sqlite:///' + os.path.join(project_root, 'test.db')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        """Required for Flask-Testing"""
        app = application.app
        app.config['TESTING'] = True
        return app

    def test_get_index(self):
        r = self.client.get("/")
        self.assert200(r)

    def test_redirect_unauthenticated_user(self):
        r = self.client.get(url_for("location.index_view"))
        expected = url_for("security.login",
                           next=url_for("location.index_view",
                                        _external=True))
        self.assertRedirects(r, expected)
