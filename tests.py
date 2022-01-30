from http import HTTPStatus
import unittest
from main import app, db
import json


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        self.db = db

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

    def test_create_then_find_then_delete_product(self):
        product_response = self.client.post('/product', data=json.dumps(dict(name='whey', price=120.99)), content_type='application/json')
        self.assertEqual(HTTPStatus.CREATED, product_response.status_code), 'assert response status code is created'
        self.assertTrue(product_response.is_json), 'assert response is json'
        self.assertEqual(dict, type(product_response.json)), 'assert response is dict'
        product_id = product_response.json['id']

        product_response = self.client.get(f'/product/{product_id}')
        self.assertTrue('whey' in product_response.json['name'])

        product_response = self.client.delete(f'/product/{product_id}')
        self.assertTrue(HTTPStatus.ACCEPTED, product_response.status_code)

    def test_create_product_invalid_request(self):
        product_response = self.client.post('/product', data=dict(nam='whey', price=120.99))
        self.assertEqual(HTTPStatus.BAD_REQUEST, product_response.status_code)
        self.assertTrue('name' in product_response.json)
        self.assertTrue(product_response.is_json)


if __name__ == '__main__':
    unittest.main()
