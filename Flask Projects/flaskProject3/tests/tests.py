import unittest
from flask import current_app
from FlaskProject import create_app, db
from FlaskProject.models import User, Permission


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app = self.app.test_client()

    def testLanding(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test418(self):
        response = self.app.post('/teapot')
        self.assertEqual(response.status_code, 418)

    def test404(self):
        response = self.app.post('/err')
        self.assertEqual(response.status_code, 404)

    def testAnonAdd(self):
        response = self.app.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You do not have permission to access this page.", response.data)

    def testAnonCart(self):
        response = self.app.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You do not have permission to access this page.", response.data)

    def testNewUser(self):
        user = User(email='test@test.com')
        user.set_password = "test"
        self.assertFalse(user.confirmed)
        self.assertTrue(user.permission == Permission.USER)
