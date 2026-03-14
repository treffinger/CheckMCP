import unittest
from unittest.mock import patch

from cmk_client.exceptions import RequestError, ResourceNotFoundError
from handlers.tools.downtime import Downtime
from input_validator.exceptions import InvalidInputError
from models import Downtime as DowntimeModel
from tests.base_test_case import BaseTestCase
from tests.handler_helpers import HANDLER_CLIENT, HANDLER_CONFIG, make_mock_config, make_mock_mcp

VALIDATOR = "handlers.tools.downtime.InputValidator"


def _make_downtime():
    return DowntimeModel.model_construct(
        id="1",
        title="My Downtime",
        comment="Maintenance",
        host_name="myhost",
        is_service="no",
        author="admin",
        start_time="2024-01-01T00:00:00Z",
        end_time="2024-01-02T00:00:00Z",
        recurring="no",
    )


class TestDowntimeHandlerListDowntimes(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_all_downtimes_returns_list(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [_make_downtime()]

        result = Downtime(self.mock_mcp).list_downtimes()

        self.assertIsInstance(result, list)

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_downtimes_by_host_passes_query_param(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_hostname.return_value = "myhost"
        mock_client = mock_client_cls.return_value
        mock_client.get.return_value = [_make_downtime()]

        Downtime(self.mock_mcp).list_downtimes(host_name="myhost")

        call_kwargs = mock_client.get.call_args[1]
        self.assertIn("query", call_kwargs.get("params", {}))

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_downtimes_invalid_hostname_returns_error(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_hostname.side_effect = InvalidInputError

        result = Downtime(self.mock_mcp).list_downtimes(host_name="invalid<host>")

        self.assertEqual(result, {"error": "Input not allowed."})
        mock_client_cls.return_value.get.assert_not_called()

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_downtimes_request_error_returns_error(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = Downtime(self.mock_mcp).list_downtimes()

        self.assertEqual(result, {"error": "An internal Server Error occurred."})

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_downtimes_result_contains_only_id_title_hostname(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [_make_downtime()]

        result = Downtime(self.mock_mcp).list_downtimes()

        self.assertEqual(set(result[0].keys()), {"id", "title", "host_name"})


class TestDowntimeHandlerGetDowntime(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_downtime_returns_dict(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_downtime_id.return_value = "1"
        mock_client_cls.return_value.get.return_value = _make_downtime()

        result = Downtime(self.mock_mcp).get_downtime("1")

        self.assertIsInstance(result, dict)

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_downtime_invalid_id_returns_error(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_downtime_id.side_effect = InvalidInputError

        result = Downtime(self.mock_mcp).get_downtime("invalid<id>")

        self.assertEqual(result, {"error": "Input not allowed."})
        mock_client_cls.return_value.get.assert_not_called()

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_downtime_not_found_returns_error(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_downtime_id.return_value = "999"
        mock_client_cls.return_value.get.side_effect = ResourceNotFoundError()

        result = Downtime(self.mock_mcp).get_downtime("999")

        self.assertEqual(result, {"error": "Downtime not found."})

    @patch(VALIDATOR)
    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_get_downtime_request_error_returns_error(self, mock_client_cls, mock_config_cls, mock_validator):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_validator.validate_downtime_id.return_value = "1"
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = Downtime(self.mock_mcp).get_downtime("1")

        self.assertEqual(result, {"error": "An internal Server Error occurred."})


if __name__ == "__main__":
    unittest.main()
