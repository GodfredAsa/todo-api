


from tests.unit.unit_base_test import UnitBaseTest
from utils.auth_utils import validate_preferred_name


class TestAuthUtils(UnitBaseTest):
    def test_validate_preferred_name_valid(self):
        valid_names = [
            "JohnDoe",
            "Jane-Doe",
            "Alice O'Connor",
            "Bob Smith",
            "Charlie123",
            "David 456",
            "Eve-789",
            "Frank O'Neil",
            "Grace Hopper",
            "Henry Ford",
        ]
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(validate_preferred_name(name))

    def test_validate_preferred_name_invalid(self):
        invalid_names = [
            "David_456",
            "John@Doe",
            "Jane#Doe",
            "Alice!",
            "Bob$",
            "Charlie%",
            "David^",
            "Eve&",
            "Frank*",
            "Grace(",
            "Henry)",
            " John",
            "John ",
            "",
        ]
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(validate_preferred_name(name))
