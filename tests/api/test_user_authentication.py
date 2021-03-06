from tests.test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from app import generate_token
from app.models import Users
from app import app, db
import unittest
import json


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI
        db.session.add(Users(id=1, email='monoliza@google.com', password_hash=generate_password_hash('igrauchu'),
                             token=generate_token.generate_token()))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful(self):
        response = self.tester.post('/api/authentication', data=json.dumps({
            'email': 'monoliza@google.com', 'password': 'igrauchu'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_data(as_text=True))

    def test_error(self):
        response = self.tester.post('/api/authentication')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("The form of the submitted json is not correct.", response.get_data(as_text=True))

    def test_error1(self):
        response = self.tester.post('/api/authentication', data=json.dumps({
            'email': 'monoliza@google.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("The form of the submitted json is not correct.", response.get_data(as_text=True))

    def test_error2(self):
        response = self.tester.post('/api/authentication', data=json.dumps({
            'password': 'igrauchu'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("The form of the submitted json is not correct.", response.get_data(as_text=True))

    def test_error3(self):
        response = self.tester.post('/api/authentication', data=json.dumps({
            'email': 'igoryan@ghjdf.ru', 'password': 'igrauchu'}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual("This email not found", response.get_data(as_text=True))

    def test_error4(self):
        response = self.tester.post('/api/authentication', data=json.dumps({
            'email': 'monoliza@google.com', 'password': 'igrauchu345'}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual("Email or password is incorrect", response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
