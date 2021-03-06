from tests.test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from app.models import Quote, Users
from app import app, db
import unittest
import json

"""Тестирование функции send_all_quote_id_which_add_user()"""


class SendQuoteTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI

        quote = Quote(user_id=1, quote_id=1,
                      author='Рэй Брэдбери', book_title='Вино из одуванчиков',
                      quote='Что хочешь помнить, то всегда помнишь.')
        db.session.add(quote)
        quote2 = Quote(user_id=1, quote_id=2,
                       author='Л.Н.Толстой', book_title='Война и мир', quote='Навсегда ничего не бывает.')
        db.session.add(quote2)
        quote3 = Quote(user_id=1, quote_id=3,
                       author='Эрих Мария Ремарк', book_title='Ночь в Лиссабоне',
                       quote='Она еще не сдалась, но уже не боролась.')
        db.session.add(quote3)
        db.session.add(Users(id=1, email='monoliza@google.com', password_hash=generate_password_hash('igrauchu'),
                             token='sfgasgasgasgdasgf'))
        db.session.add(Users(id=2, email='monoliza45@google.com', password_hash=generate_password_hash('igrauchu123'),
                             token='dsgsdfdsfs'))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_send_all_quote_id_which_add_user(self):
        """Тестирование функции send_all_quote_id_which_add_user()"""
        token = Users.query.filter_by(email='monoliza@google.com').first().token
        response = self.tester.post('/api/all_quotes', data=json.dumps({
            'token': token}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(3, len(json_response))

    def test_send_all_quote_id_which_add_user_error(self):
        """Тестирование функции send_all_quote_id_which_add_user(), у пользователя нет добавленных цитат"""
        token = Users.query.filter_by(email='monoliza45@google.com').first().token
        response = self.tester.post('/api/all_quotes', data=json.dumps({
            'token': token}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('You not add quotes', response.get_data(as_text=True))

    def test_send_all_quote_id_which_add_user_error2(self):
        """Тестирование функции send_all_quote_id_which_add_user(), пользователь не отправил данные токена"""
        response = self.tester.post('/api/all_quotes')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_send_all_quote_id_which_add_user_error3(self):
        """Тестирование функции send_all_quote_id_which_add_user(), такого токена нет в базу данных"""
        response = self.tester.post('/api/all_quotes', data=json.dumps({
            'token': 'skdjvkpasdvvkpasd'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
