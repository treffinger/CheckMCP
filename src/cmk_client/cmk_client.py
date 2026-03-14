from __future__ import annotations

import logging
from typing import Any, ClassVar

import requests
from pydantic import BaseModel, ValidationError
from requests import Response
from requests.exceptions import JSONDecodeError

from config import ConfigLoader

from .exceptions import RequestError, ResourceNotFoundError


class CmkClient:
    _instance: ClassVar[CmkClient | None] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls) -> CmkClient:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if CmkClient._initialized:
            return
        config = ConfigLoader.get_config()
        self._base_url = self._prepare_api_url(str(config.cmk_url), config.cmk_site)
        # NOTE: Checkmk uses a non-standard Bearer format that includes both username and password
        # instead of a single token. This is intentional and required by the Checkmk REST API.
        self._headers = {"Authorization": f"Bearer {config.cmk_username} {config.cmk_password}"}
        CmkClient._initialized = True

    def get(
        self, path: str, validation_model: type[BaseModel], *, list_key: str | None = None, params: dict | None = None
    ) -> Any:
        response = requests.get(url=f"{self._base_url}{path}", headers=self._headers, params=params, timeout=10)

        if response.status_code == 404:
            raise ResourceNotFoundError
        elif not response.ok:
            logging.error(f"The checkmk API returned an error: {response.text}")
            raise RequestError

        data = self._require_dictionary(response)

        if list_key is None:
            return self._get_model_or_raise(data, validation_model)

        if list_key not in data or not isinstance(data[list_key], list):
            raise RequestError

        return [self._get_model_or_raise(m, validation_model) for m in data[list_key]]

    def _get_model_or_raise(self, data: dict, validation_model: type[BaseModel]) -> BaseModel:
        try:
            return validation_model.model_validate(data)
        except ValidationError as e:
            logging.error(
                f'Error while validating checkmk API response. Validation of the model "{validation_model.__name__}" failed. Error: {e}'
            )
            raise RequestError from e

    def _prepare_api_url(self, host: str, site: str) -> str:
        if not host.endswith("/"):
            host += "/"

        return f"{host}{site}/check_mk/api/1.0"

    def _require_dictionary(self, response: Response) -> dict:
        try:
            data = response.json()
        except JSONDecodeError as e:
            raise RequestError from e

        if not isinstance(data, dict):
            raise RequestError

        return data
