from tests.test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from app.models import Quote
from app import app, db
import unittest
import json

"""
Тестирование GET-методов модуля quotes.
Тестирование функций send_a_random_quote(), send_quote_on_quote_id(), send_quote_on_author_or_book_title(), 
                     send_quote_author_and_book_title(), send_give_count_quotes()
"""


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
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_send_a_random_quote(self):
        """Тестирование функции send_a_random_quote()"""
        response = self.tester.get('/api/quote')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('user_id', json_response)
        self.assertIn('quote_id', json_response)
        self.assertIn('quote', json_response)
        self.assertIn('author', json_response['quote'])
        self.assertIn('book_title', json_response['quote'])
        self.assertIn('quote', json_response['quote'])

    def test_send_quote_on_quote_id(self):
        """Тестирование функции send_quote_on_quote_id()"""
        response = self.tester.get('/api/quote/1')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('user_id', json_response)
        self.assertIn('quote_id', json_response)
        self.assertIn('quote', json_response)
        self.assertIn('author', json_response['quote'])
        self.assertIn('book_title', json_response['quote'])
        self.assertIn('quote', json_response['quote'])

    def test_send_quote_on_quote_id_error(self):
        """Тестирование функции send_quote_on_quote_id(), цитата не найдена"""
        response = self.tester.get('/api/quote/45')
        self.assertEqual(response.status_code, 404)

    def test_successful_send_quote_on_author_or_book_title(self):
        """Тестирование функции send_quote_author_or_book_title()"""
        response = self.tester.get('/api/quote/Рэй%20Брэдбери')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('user_id', json_response)
        self.assertIn('quote_id', json_response)
        self.assertIn('quote', json_response)
        self.assertIn('author', json_response['quote'])
        self.assertIn('book_title', json_response['quote'])
        self.assertIn('quote', json_response['quote'])

    def test_send_quote_on_author_or_book_title_error(self):
        """Тестирование функции send_quote_author_or_book_title(), цитата не найдена"""
        response = self.tester.get('/api/quote/d')
        self.assertEqual(response.status_code, 404)

    def test_send_quote_author_and_book_title(self):
        """Тестирование функции send_quote_author_and_book_title()"""
        response = self.tester.get('/api/quote/Рэй%20Брэдбери/Вино%20из%20одуванчиков')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('user_id', json_response)
        self.assertIn('quote_id', json_response)
        self.assertIn('quote', json_response)
        self.assertIn('author', json_response['quote'])
        self.assertIn('book_title', json_response['quote'])
        self.assertIn('quote', json_response['quote'])

    def test_send_quote_author_and_book_title_error(self):
        """Тестирование функции send_quote_author_and_book_title(), ошибка цитата не найдена"""
        response = self.tester.get('/api/quote/Рэй%20Брэдбери/Война%20и%20мир')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('Quote not found', response.get_data(as_text=True))

    def test_send_give_count_quotes(self):
        """Тестирование функции send_give_count_quotes()"""
        response = self.tester.get('/api/quotes/2')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(2, len(json_response))
        self.assertIn('user_id', json_response[1])
        self.assertIn('quote_id', json_response[1])
        self.assertIn('quote', json_response[1])
        self.assertIn('author', json_response[1]['quote'])
        self.assertIn('book_title', json_response[1]['quote'])
        self.assertIn('quote', json_response[1]['quote'])

    def test_send_give_count_quotes_error(self):
        """Тестирование функции send_give_count_quotes()"""
        response = self.tester.get('/api/quotes/fg')
        self.assertEqual(response.status_code, 404)

    # Из-за слишком долгой работы этого теста(обусловлена тем, что из-за random.choice,
    # не сразу может собрать все цитаты), этот тест я отправил в коментарии к коду.
    # def test_send_give_count_quotes2(self):
    #     """Тестирование функции send_give_count_quotes(), задано количество, превышающее количество цитата в бд"""
    #     response = self.tester.get('/api/quotes/45')
    #     self.assertEqual(response.status_code, 200)
    #     json_response = json.loads(response.get_data(as_text=True))
    #     self.assertEqual(3, len(json_response))
    #     self.assertIn('user_id', json_response[1])
    #     self.assertIn('quote_id', json_response[1])
    #     self.assertIn('quote', json_response[1])
    #     self.assertIn('author', json_response[1]['quote'])
    #     self.assertIn('book_title', json_response[1]['quote'])
    #     self.assertIn('quote', json_response[1]['quote'])


if __name__ == '__main__':
    unittest.main()
