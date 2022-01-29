from http import HTTPStatus
import unittest
from main import app


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()

    def tearDown(self) -> None:
        pass

    def test_product(self):
        product_response = self.client.get('/product')
        self.assertEqual(HTTPStatus.OK, product_response.status_code)
        self.assertTrue(product_response.is_json)
        self.assertEqual(list, type(product_response.json))

    def test_find_product(self):
        product_response = self.client.get('/product/1')
        self.assertEqual(HTTPStatus.OK, product_response.status_code)
        self.assertTrue(product_response.is_json)
        self.assertEqual(dict, type(product_response.json))

    def test_create_product(self):
        product_response = self.client.post('/product', data=dict(name='whey', price=120.99))
        self.assertEqual(HTTPStatus.CREATED, product_response.status_code) , 'assert response status code is created'
        self.assertTrue(product_response.is_json) , 'assert response is json'
        self.assertEqual(dict, type(product_response.json)), 'assert response is dict'

        product_response = self.client.get('/product/3')
        self.assertTrue('whey' in product_response.json['name'])
    
    def test_create_product_invalid_request(self):
        product_response = self.client.post('/product', data=dict(nam='whey', price=120.99))
        self.assertEqual(HTTPStatus.BAD_REQUEST, product_response.status_code)
        self.assertTrue('name' in product_response.json)
        self.assertTrue(product_response.is_json)


if __name__ == '__main__':
    unittest.main()
