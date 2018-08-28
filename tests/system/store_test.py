from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)

                response = client.post('/store/test')
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'test' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)

                response = client.delete('/store/test')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': "Store deleted"}, json.loads(response.data))
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)

                response = client.get('/store/test')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data)['name'], 'test')
                #{'name': self.name, 'items': [item.json() for item in self.items.all()]}

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': "Store not found."}, json.loads(response.data))

                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)

                response = client.get('/store/test2')
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': "Store not found."}, json.loads(response.data))

                response = client.delete('/store/test')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': "Store deleted"}, json.loads(response.data))

                response = client.get('/store/test')
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': "Store not found."}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)

                client.post('/item/test_item', data={'price': 12, 'store_id': 1})

                response = client.get('/store/test')
                self.assertEqual(response.status_code, 200)
                store_dict = json.loads(response.data)
                self.assertDictEqual(store_dict,
                                     {'name': 'test', 'items': [{'name':'test_item', 'price': 12}]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.post('/store/test2')
                self.assertEqual(response.status_code, 201)


                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                stores_dict = json.loads(response.data)
                self.assertDictEqual(stores_dict,
                                     {'stores': [{'name': 'test', 'items': []},
                                                 {'name': 'test2', 'items': []}]})

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)
                response = client.post('/store/test2')
                self.assertEqual(response.status_code, 201)

                client.post('/item/test_item', data={'price': 12, 'store_id': 1})
                client.post('/item/test_item1', data={'price': 13, 'store_id': 2})
                client.post('/item/test_item2', data={'price': 18, 'store_id': 2})

                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                stores_dict = json.loads(response.data)
                self.assertDictEqual(stores_dict,
                                     {'stores': [{'name': 'test', 'items': [{'name': 'test_item', 'price': 12}]},
                                                 {'name': 'test2', 'items': [{'name': 'test_item1', 'price': 13},
                                                                             {'name': 'test_item2', 'price': 18}]}]})