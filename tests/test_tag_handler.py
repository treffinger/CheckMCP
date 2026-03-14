import unittest
from unittest.mock import patch

from cmk_client.exceptions import RequestError
from handlers.tools.tag import Tag as TagHandler
from models import HostTagGroup, Tag
from tests.base_test_case import BaseTestCase
from tests.handler_helpers import HANDLER_CLIENT, HANDLER_CONFIG, make_mock_config, make_mock_mcp


def make_tag_group():
    return HostTagGroup.model_construct(
        name="criticality",
        title="Criticality",
        tags=[Tag.model_construct(name="prod", title="Production"), Tag.model_construct(name="test", title="Test")],
    )


class TestTagHandler(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_mcp = make_mock_mcp()
        self.mock_config = make_mock_config()

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_tags_returns_list_of_dicts(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [make_tag_group()]
        result = TagHandler(self.mock_mcp).list_tags()
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], dict)

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_tags_result_contains_name_and_title(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [make_tag_group()]
        result = TagHandler(self.mock_mcp).list_tags()
        self.assertEqual(result[0]["name"], "criticality")
        self.assertEqual(result[0]["title"], "Criticality")

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_tags_result_contains_tags_list(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = [make_tag_group()]
        result = TagHandler(self.mock_mcp).list_tags()
        self.assertEqual(len(result[0]["tags"]), 2)

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_tags_empty_result(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.return_value = []
        result = TagHandler(self.mock_mcp).list_tags()
        self.assertEqual(result, [])

    @patch(HANDLER_CONFIG)
    @patch(HANDLER_CLIENT)
    def test_list_tags_request_error_returns_error_dict(self, mock_client_cls, mock_config_cls):
        mock_config_cls.get_config.return_value = self.mock_config
        mock_client_cls.return_value.get.side_effect = RequestError()

        result = TagHandler(self.mock_mcp).list_tags()

        self.assertEqual(result, {"error": "An internal Server Error occurred."})


if __name__ == "__main__":
    unittest.main()
