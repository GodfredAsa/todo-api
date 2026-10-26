
from tests.unit.unit_base_test import UnitBaseTest
from utils.api_response import CustomApiResponse


class TestApiResponse(UnitBaseTest):
    def test_custom_api_response(self):
        response = CustomApiResponse.get_response(
            message="Test message",
            status=200,
            data={"key": "value"},  
        )
        self.assertEqual(response["message"], "Test message")
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"], {"key": "value"})

    def test_custom_api_response_default_data(self):
        response = CustomApiResponse.get_response(
            message="Test message",
            status=200,
            data=None,
        )
        self.assertEqual(response["message"], "Test message")
        self.assertEqual(response["status"], 200)
        self.assertIsNone(response["data"])