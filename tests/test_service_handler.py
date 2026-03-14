import unittest
from unittest.mock import patch

from cmk_client.exceptions import RequestError, ResourceNotFoundError
from handlers.tools.service import Service
from input_validator.exceptions import InvalidInputError
from models import Service as ServiceModel
from tests.base_test_case import BaseTestCase
from tests.handler_helpers import HANDLER_CLIENT, HANDLER_CONFIG, make_mock_config, make_mock_mcp

VALIDATOR = "handlers.tools.service.InputValidator"


class TestServiceHandler(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_services_returns_list(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_hostname.return_value = "myhost"
        mock_client_cls.return_value.get.return_value = [
            ServiceModel(id="svc_1", title="CPU"),
            ServiceModel(id="svc_2", title="Memory"),
        ]

        result = Service(self.mock_mcp).get_host_services("myhost")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_services_invalid_hostname_returns_error(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_hostname.side_effect = InvalidInputError

        result = Service(self.mock_mcp).get_host_services("invalid<host>")

        self.assertEqual(result, {"error": "Input not allowed."})
        mock_client_cls.return_value.get.assert_not_called()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_services_not_found_returns_error(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_hostname.return_value = "unknown"
        mock_client_cls.return_value.get.side_effect = ResourceNotFoundError()

        result = Service(self.mock_mcp).get_host_services("unknown")

        self.assertEqual(result, {"error": "Host not found."})

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_services_request_error_returns_error(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_hostname.return_value = "myhost"
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = Service(self.mock_mcp).get_host_services("myhost")

        self.assertEqual(result, {"error": "An internal Server Error occurred."})


if __name__ == "__main__":
    unittest.main()
