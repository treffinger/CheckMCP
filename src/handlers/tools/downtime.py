import json
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from cmk_client.exceptions import RequestError, ResourceNotFoundError
from input_validator import InputValidator
from input_validator.exceptions import InvalidInputError
from models import Downtime as DowntimeModel
from models import Error

from ..handler import Handler


class Downtime(Handler):
    def __init__(self, mcp: FastMCP) -> None:
        super().__init__()
        mcp.tool(description="Returns all scheduled downtimes")(self.list_downtimes)
        mcp.tool(description="Returns a specific downtime with more details")(self.get_downtime)

    def list_downtimes(self, host_name: str | None = None) -> list[dict] | dict:
        if host_name is not None:
            try:
                InputValidator.validate_hostname(host_name)
            except InvalidInputError:
                return Error(error="Input not allowed.").model_dump()

        downtimes: list[DowntimeModel] = []
        try:
            if host_name is None:
                downtimes = self._get_all_downtimes()
            else:
                downtimes = self._search_downtime_for_host(host_name)
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()

        return [downtime.model_dump(include={"id", "title", "host_name"}) for downtime in downtimes]

    def get_downtime(self, downtime_id: str) -> dict:
        try:
            InputValidator.validate_downtime_id(downtime_id)
        except InvalidInputError:
            return Error(error="Input not allowed.").model_dump()

        site = self._config.cmk_site
        try:
            downtime: DowntimeModel = self._client.get(
                f"/objects/downtime/{downtime_id}", DowntimeModel, params={"site_id": site}
            )
        except ResourceNotFoundError:
            return Error(error="Downtime not found.").model_dump()
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()

        return downtime.model_dump(include=self._config.downtime_object_attributes)

    def _get_all_downtimes(self) -> list[DowntimeModel]:
        return self._client.get("/domain-types/downtime/collections/all", DowntimeModel, list_key="value")

    def _search_downtime_for_host(self, host_name: str) -> list[DowntimeModel]:
        query = {"op": "=", "left": "host_name", "right": host_name}
        return self._client.get(
            "/domain-types/downtime/collections/all",
            DowntimeModel,
            list_key="value",
            params={"query": json.dumps(query)},
        )
