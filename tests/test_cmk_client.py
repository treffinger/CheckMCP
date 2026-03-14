import unittest
from typing import cast
from unittest.mock import MagicMock, patch

from pydantic import BaseModel
from requests.exceptions import JSONDecodeError

from cmk_client.cmk_client import CmkClient
from cmk_client.exceptions import RequestError, ResourceNotFoundError
from tests.base_test_case import BaseTestCase


class SimpleModel(BaseModel):
    name: str


CONFIG_PATCH = "cmk_client.cmk_client.ConfigLoader"
REQUESTS_PATCH = "cmk_client.cmk_client.requests.get"


def _make_mock_config(url="https://checkmk.example.com", site="mysite"):
    config = MagicMock()
    config.cmk_url = url
    config.cmk_site = site
    config.cmk_username = "automation"
    config.cmk_password = "secret"
    return config


class TestCmkClient(BaseTestCase):
    def setUp(self):
        super().setUp()
        with patch(CONFIG_PATCH) as mock_cfg:
            mock_cfg.get_config.return_value = _make_mock_config()
            self.client = CmkClient()

    # Singleton

    def test_singleton_two_instances_are_identical(self):
        with patch(CONFIG_PATCH) as mock_cfg:
            mock_cfg.get_config.return_value = _make_mock_config()
            second = CmkClient()
        self.assertIs(self.client, second)

    def test_singleton_is_reset_between_tests(self):
        self.assertIsNotNone(CmkClient._instance)

    # _prepare_api_url

    def test_prepare_api_url_without_trailing_slash(self):
        with patch(CONFIG_PATCH) as mock_cfg:
            mock_cfg.get_config.return_value = _make_mock_config(url="https://checkmk.example.com", site="mysite")
            client = CmkClient()
        self.assertEqual(
            client._base_url,
            "https://checkmk.example.com/mysite/check_mk/api/1.0",
        )

    def test_prepare_api_url_keeps_trailing_slash(self):
        with patch(CONFIG_PATCH) as mock_cfg:
            mock_cfg.get_config.return_value = _make_mock_config(url="https://checkmk.example.com/", site="mysite")
            client = CmkClient()
        self.assertEqual(
            client._base_url,
            "https://checkmk.example.com/mysite/check_mk/api/1.0",
        )

    # _require_dictionary

    def test_require_dictionary_returns_valid_json_dict(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        result = self.client._require_dictionary(mock_response)
        self.assertEqual(result, {"key": "value"})

    def test_require_dictionary_raises_on_non_dict_json(self):
        mock_response = MagicMock()
        mock_response.json.return_value = ["a", "b"]
        with self.assertRaises(RequestError):
            self.client._require_dictionary(mock_response)

    def test_require_dictionary_raises_on_invalid_json(self):
        mock_response = MagicMock()
        mock_response.json.side_effect = JSONDecodeError("", "", 0)
        with self.assertRaises(RequestError):
            self.client._require_dictionary(mock_response)

    # _get_model_or_raise

    def test_get_model_or_raise_returns_model_instance(self):
        result = self.client._get_model_or_raise({"name": "test"}, SimpleModel)
        self.assertIsInstance(result, SimpleModel)
        result = cast(SimpleModel, result)
        self.assertEqual(result.name, "test")

    def test_get_model_or_raise_raises_on_invalid_data(self):
        with self.assertRaises(RequestError):
            self.client._get_model_or_raise({"wrong_field": "value"}, SimpleModel)

    # get

    def _make_ok_response(self, body):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = body
        return mock_response

    def test_get_returns_model_on_success(self):
        with patch(REQUESTS_PATCH, return_value=self._make_ok_response({"name": "myhost"})):
            result = self.client.get("/objects/host/myhost", SimpleModel)
        self.assertIsInstance(result, SimpleModel)
        self.assertEqual(result.name, "myhost")

    def test_get_raises_resource_not_found_on_404(self):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.ok = False
        with patch(REQUESTS_PATCH, return_value=mock_response):
            with self.assertRaises(ResourceNotFoundError):
                self.client.get("/objects/host/unknown", SimpleModel)

    def test_get_raises_request_error_on_server_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.ok = False
        mock_response.text = "Internal Server Error"
        with patch(REQUESTS_PATCH, return_value=mock_response):
            with self.assertRaises(RequestError):
                self.client.get("/some/path", SimpleModel)

    def test_get_with_list_key_returns_list_of_models(self):
        body = {"value": [{"name": "host1"}, {"name": "host2"}]}
        with patch(REQUESTS_PATCH, return_value=self._make_ok_response(body)):
            result = self.client.get("/domain-types/host/collections/all", SimpleModel, list_key="value")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(r, SimpleModel) for r in result))

    def test_get_raises_when_list_key_is_missing(self):
        body = {"other_key": []}
        with patch(REQUESTS_PATCH, return_value=self._make_ok_response(body)):
            with self.assertRaises(RequestError):
                self.client.get("/some/path", SimpleModel, list_key="value")

    def test_get_raises_when_list_key_value_is_not_a_list(self):
        body = {"value": "not-a-list"}
        with patch(REQUESTS_PATCH, return_value=self._make_ok_response(body)):
            with self.assertRaises(RequestError):
                self.client.get("/some/path", SimpleModel, list_key="value")

    def test_get_passes_params_to_request(self):
        body = {"name": "myhost"}
        with patch(REQUESTS_PATCH, return_value=self._make_ok_response(body)) as mock_req:
            self.client.get("/objects/host/myhost", SimpleModel, params={"columns": ["state"]})
        _, kwargs = mock_req.call_args
        self.assertEqual(kwargs["params"], {"columns": ["state"]})


if __name__ == "__main__":
    unittest.main()
