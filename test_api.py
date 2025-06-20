import unittest
import requests

BASE_URL = 'http://127.0.0.1:5000'

class TestUserAPI(unittest.TestCase):
    def test_01_add_user(self):
        data = {'name': '张三', 'age': 20}
        r = requests.post(f'{BASE_URL}/user', json=data)
        self.assertEqual(r.status_code, 201)
        self.assertIn('id', r.json())
        self.__class__.user_id = r.json()['id']

    def test_02_get_users(self):
        r = requests.get(f'{BASE_URL}/users')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        self.assertTrue(any(u['name'] == '张三' for u in r.json()))

    def test_03_get_user(self):
        r = requests.get(f'{BASE_URL}/user/{self.__class__.user_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['name'], '张三')

    def test_04_update_user(self):
        data = {'name': '李四', 'age': 22}
        r = requests.put(f'{BASE_URL}/user/{self.__class__.user_id}', json=data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['name'], '李四')

    def test_05_delete_user(self):
        r = requests.delete(f'{BASE_URL}/user/{self.__class__.user_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['message'], 'User deleted')

    def test_06_get_user_not_found(self):
        r = requests.get(f'{BASE_URL}/user/99999')
        self.assertEqual(r.status_code, 404)
        self.assertIn('error', r.json())

if __name__ == '__main__':
    unittest.main()
