from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_create_user(self):
        user = UserModel('test', 'password')

        self.assertEqual(user.username, 'test', "error message")
        self.assertEqual(user.password, 'password', 'error message')