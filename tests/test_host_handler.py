import unittest
from unittest.mock import patch

from cmk_client.exceptions import RequestError, ResourceNotFoundError
from handlers.tools.host import Host
from input_validator.exceptions import InvalidInputError
from models import Host as HostModel
from tests.base_test_case import BaseTestCase
from tests.handler_helpers import HANDLER_CLIENT, HANDLER_CONFIG, make_mock_config, make_mock_mcp

VALIDATOR = "handlers.tools.host.InputValidator"
FORMAT_CONVERTER = "handlers.tools.host.FormatConverter"


class TestHostHandlerListHosts(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_all_hosts_returns_name_list(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [
            HostModel.model_construct(name="host1"),
            HostModel.model_construct(name="host2"),
        ]
        result = Host(self.mock_mcp).list_hosts()
        self.assertEqual(result, [{"name": "host1"}, {"name": "host2"}])

    @patch(FORMAT_CONVERTER)
    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_hosts_by_folder_normalizes_path(
        self, mock_client_cls, mock_config_cls, mock_validator, mock_converter
    ):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_converter.normalize_folder_path.return_value = "~linux~servers"
        mock_client = mock_client_cls.return_value
        mock_client.get.return_value = []

        Host(self.mock_mcp).list_hosts(folder_path="/linux/servers")

        mock_validator.validate_folder_path.assert_called_once_with("/linux/servers")
        mock_converter.normalize_folder_path.assert_called_once_with("/linux/servers")
        call_path = mock_client.get.call_args[0][0]
        self.assertIn("~linux~servers", call_path)

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_hosts_invalid_folder_returns_error_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_folder_path.side_effect = InvalidInputError

        result = Host(self.mock_mcp).list_hosts(folder_path="invalid<input>")

        self.assertEqual(result, {"error": "Input not allowed."})
        mock_client_cls.return_value.get.assert_not_called()

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_hosts_request_error_returns_error_dict(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = Host(self.mock_mcp).list_hosts()

        self.assertEqual(result, {"error": "An internal Server Error occurred."})


class TestHostHandlerGetHost(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_returns_host_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = HostModel.model_construct(name="myhost", alias="My Host")

        result = Host(self.mock_mcp).get_host("myhost")

        mock_validator.validate_hostname.assert_called_once_with("myhost")
        self.assertEqual(result["name"], "myhost")

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_invalid_name_returns_error_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_hostname.side_effect = InvalidInputError

        result = Host(self.mock_mcp).get_host("invalid<name>")

        self.assertEqual(result, {"error": "Input not allowed."})
        mock_client_cls.return_value.get.assert_not_called()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_not_found_returns_error_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.side_effect = ResourceNotFoundError()

        result = Host(self.mock_mcp).get_host("unknown")

        self.assertEqual(result, {"error": "Host not found."})

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_host_request_error_returns_error_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = Host(self.mock_mcp).get_host("myhost")

        self.assertEqual(result, {"error": "An internal Server Error occurred."})


class TestHostHandlerSearchHost(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_search_host_returns_host_list(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [
            HostModel.model_construct(name="host1", alias="Host 1"),
            HostModel.model_construct(name="host2", alias="Host 2"),
        ]

        result = Host(self.mock_mcp).search_host(filter={"address": "192\\.168\\..*"})

        mock_validator.validate_search_filter.assert_called_once_with({"address": "192\\.168\\..*"})
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "host1")
        self.assertEqual(result[1]["name"], "host2")

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_search_host_invalid_filter_returns_error_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_search_filter.side_effect = InvalidInputError

        result = Host(self.mock_mcp).search_host(filter={"<invalid>": "value"})

        self.assertEqual(result, {"error": "Input not allowed."})
        mock_client_cls.return_value.get.assert_not_called()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_search_host_request_error_returns_error_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = Host(self.mock_mcp).search_host(filter={"address": "192\\.168\\..*"})

        self.assertEqual(result, {"error": "An internal Server Error occurred."})

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_search_host_builds_correct_filter_query(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = []

        Host(self.mock_mcp).search_host(filter={"address": "10\\..*", "tag_names": "prod"})

        call_params = mock_client_cls.return_value.get.call_args
        query_param = call_params[1]["params"]["query"]
        self.assertIn("address", query_param)
        self.assertIn("tag_names", query_param)


if __name__ == "__main__":
    unittest.main()
