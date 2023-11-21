import json
import unittest

import requests

from main import app

client = app.test_client()


class TestMain(unittest.TestCase):

    def test_register(self):
        myobj = {
            "name": "Maxi Muster",
            "password": "sicherespasswort",
            "email": "max2.muster@gmail.com",
            "location": "Neuer Wall 11, Hamburg",
            "age": 21
        }

        req = client.post('/api/user/register', data=myobj)

        res = json.loads(req.data)
        self.assertEqual(res, {"status": 201})

    def test_login(self):
        myobj = {
            "password": "sicherespasswort",
            "email": "max2.muster@gmail.com",

        }

        req = client.post("/api/user/login", data=myobj)

        res = json.loads(req.data)
        self.assertEqual(res, {'status': 200})

    def test_login_after_delete(self):
        myobj = {
            "password": "sicherespasswort",
            "email": "max2.muster@gmail.com",

        }

        req = requests.post('api/user/login', data=myobj)

        res = json.loads(req.data)
        self.assertEqual(res, {'status': 404})

    def test_create_shoppinglist(self):
        myobj = {
            "item1": {"product": "Milk",
                      "count": "2",
                      "shopper": "100",
                      "status": "WAITING"},
            "item2": {"product": "Milk",
                      "count": "2",
                      "shopper": "100",
                      "status": "WAITING"},
            "item3": {"product": "Milk",
                      "count": "2",
                      "shopper": "100",
                      "status": "WAITING"},
            "status": False,
            "created_by": "62",
            "allow_multiple_shoppers": False
        }
        req = requests.post('/api/shoppinglist/create', data=myobj)
        res = json.loads(req.data)
        self.assertEqual(res, {'status': 201})

    def test_deleteuser(self):
        myobj = {
            "name": "Maxi Muster",
            "email": "max2.muster@gmail.com",
        }

        req = requests.post('/api/user/delete', data=myobj)
        res = json.loads(req.data)
        self.assertEqual(res, {'status': 200})

    def test_status_shoppinglist(self):
        shoppinglist_exists = self.change_status_shoppinglist()
        self.assertEqual(shoppinglist_exists, {'status': 200})
        shoppinglist_not_exist = self.change_status_shoppinglist(id=120)
        self.assertEqual(shoppinglist_not_exist, {'status': 404})

    def change_status_shoppinglist(self, id=1, status=True):
        myobj = {
            "id": id,
            "status": status,
        }
        req = requests.post('/api/shoppinglist/status', data=myobj)
        return json.loads(req.data)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestMain('test_register'))
    suite.addTest(TestMain('test_login'))
    suite.addTest(TestMain('test_deleteuser'))
    suite.addTest(TestMain('test_login_after_delete'))
    suite.addTest(TestMain('test_create_shoppinglist'))
    suite.addTest(TestMain('test_status_shoppinglist'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
