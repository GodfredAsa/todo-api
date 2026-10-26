from model.user_model import UserModel
from tests.unit.unit_base_test import UnitBaseTest
import json

class TestUserModel(UnitBaseTest):
    def test_user_model(self):
        user = UserModel(preferred_name="testuser", password="1234")
        self.assertEqual(user.preferred_name, "testuser")
        self.assertEqual(user.password, "1234")
        self.assertIsNone(user.id)

    def test_user_to_json(self):
        user = UserModel(preferred_name="testuser", password="1234")
    
        expected_user = {
            "user_id": user.user_id,
            "preferred_name": "testuser",
        }
        self.assertEqual(user.to_dict(), expected_user)

    def test_user_dict(self):
        user_dict = UserModel(preferred_name="testuser", password="1234").to_dict()
        expected_user_dict = {
            "user_id": user_dict["user_id"],
            "preferred_name": "testuser",
        }
        self.assertEqual(user_dict, expected_user_dict)
