from model.user_model import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest


class TestUserModel(IntegrationBaseTest):
    def test_create_user(self):

        with self.app_context():
            user = UserModel("user", "password")
            self.assertIsNone(UserModel.find_by_preferred_name("test@tests@com"), "fetches user by username")
            self.assertIsNone(UserModel.find_by_uuid(user.id), "fetches user by user id")
            self.assertEqual(user.password, "password", "password not hashed")
            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_preferred_name("user"), "user is saved")
            