import unittest
from unittest.mock import patch

from cmk_client.exceptions import RequestError
from handlers.tools.folder import Folder
from models import Folder as FolderModel
from tests.base_test_case import BaseTestCase
from tests.handler_helpers import HANDLER_CLIENT, HANDLER_CONFIG, make_mock_config, make_mock_mcp


def make_folder():
    return FolderModel.model_construct(
        name="Linux", path="/linux", created_at="2024-01-01T00:00:00Z", updated_at="2024-01-02T00:00:00Z"
    )


class TestFolderHandler(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_folders_returns_list_of_dicts(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [make_folder(), make_folder()]
        result = Folder(self.mock_mcp).list_folders()
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(r, dict) for r in result))

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_folders_result_contains_name_and_path(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [make_folder()]
        result = Folder(self.mock_mcp).list_folders()
        self.assertEqual(result[0]["path"], "/linux")
        self.assertEqual(result[0]["name"], "Linux")

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_folders_calls_recursive_endpoint(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client = mock_client_cls.return_value
        mock_client.get.return_value = []
        Folder(self.mock_mcp).list_folders()
        call_params = mock_client.get.call_args.kwargs["params"]
        self.assertDictEqual({"recursive": "true"}, call_params)

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_folders_request_error_returns_error_dict(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = Folder(self.mock_mcp).list_folders()

        self.assertEqual(result, {"error": "An internal Server Error occurred."})


if __name__ == "__main__":
    unittest.main()
