"""All tests"""
import json
import os

from ton import application
from ton.api import GetLocationsResource
from ton.models import db, Location
from flask.ext.testing import TestCase
from flask import url_for


class TonTests(TestCase):
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


class StatusTests(TonTests):
    def test_get_index(self):
        r = self.client.get("/")
        self.assert200(r)

    def test_redirect_unauthenticated_user(self):
        r = self.client.get(url_for("location.index_view"))
        expected = url_for("security.login",
                           next=url_for("location.index_view",
                                        _external=True))
        self.assertRedirects(r, expected)


class ApiTests(TonTests):
    # Helpers
    def create_location(self, name="Default name", **kwargs):
        loc = Location(name=name, **kwargs)
        db.session.add(loc)
        return loc

    def get_json_as_dict(self):
        r = self.client.get(self.app.api.url_for(GetLocationsResource))
        return json.loads(r.data.decode('utf-8'))

    def validate_api_string_field(self, db_field, json_field=None):
        """Create Location, get resource, parse json, assert."""
        expected = "xyzzy"
        self.create_location(**{db_field: expected})
        j = self.get_json_as_dict()
        key = json_field or db_field
        self.assertIn(key, j['locations'][0])
        self.assertEqual(j['locations'][0][key], expected)

    # Tests
    def test_location_name(self):
        self.validate_api_string_field(db_field='name')

    def test_location_description(self):
        self.validate_api_string_field(db_field='description')

    def test_location_address_line1(self):
        self.validate_api_string_field(db_field='address_line1')

    def test_location_address_line2(self):
        self.validate_api_string_field(db_field='address_line2')

    def test_location_address_line3(self):
        self.validate_api_string_field(db_field='address_line3')

    def test_location_phone(self):
        self.validate_api_string_field(db_field='phone')

    def test_location_contact_email(self):
        self.validate_api_string_field(db_field='contact_email')

    def test_location_website(self):
        self.validate_api_string_field(db_field='website')
