"""All tests"""
from ton import application
from unittest import TestCase


class StatusTest(TestCase):
    def setUp(self):
        application.app.config['TESTING'] = True
        self.app = application.app.test_client()

    def test_get_index(self):
        """Request /"""
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)
