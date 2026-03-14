import json
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from cmk_client.exceptions import RequestError, ResourceNotFoundError
from format_converter import FormatConverter
from input_validator import InputValidator
from input_validator.exceptions import InvalidInputError
from models import Error
from models import Host as HostModel

from ..handler import Handler


class Host(Handler):
    def __init__(self, mcp: FastMCP) -> None:
        super().__init__()
        mcp.tool(description="Returns all hosts, or hosts from a specific folder")(self.list_hosts)
        mcp.tool(description="Returns a host and a list of its monitored services")(self.get_host)
        mcp.tool(description="Searches hosts by the given filters")(self.search_host)

    def list_hosts(
        self,
        folder_path: (
            Annotated[str, Field(description="Path of the folder from which all hosts will be returned")] | None
        ) = None,
    ) -> list[dict] | dict:
        hosts: list[HostModel] = []
        try:
            if folder_path is not None:
                InputValidator.validate_folder_path(folder_path)
                folder_path = FormatConverter.normalize_folder_path(folder_path)
                hosts = self._search_hosts_by_folder(folder_path)
            else:
                hosts = self._get_all_hosts()
        except InvalidInputError:
            return Error(error="Input not allowed.").model_dump()
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()

        return [host.model_dump(include={"name"}) for host in hosts]

    def get_host(self, hostname: str) -> dict:
        try:
            InputValidator.validate_hostname(hostname)
            host: HostModel = self._client.get(
                f"/objects/host/{hostname}", HostModel, params={"columns": self._config.host_object_attributes}
            )
        except InvalidInputError:
            return Error(error="Input not allowed.").model_dump()
        except ResourceNotFoundError:
            return Error(error="Host not found.").model_dump()
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()

        return host.model_dump(exclude_none=True)

    def search_host(
        self,
        filter: Annotated[
            dict[str, str],
            Field(
                "Key-value pairs to filter hosts. Keys are host columns like 'address', 'tag_names', 'tag_values'."
                "Values are matched as case-sensitive regular expressions. All conditions are AND-combined. "
                r'Example: {"address": "192\.168\..*", "tag_names": "criticality", "tag_values": "prod"}'
            ),
        ],
    ) -> list[dict] | dict:
        try:
            InputValidator.validate_search_filter(filter)
            filter = self._create_filter(filter)
            hosts: list[HostModel] = self._client.get(
                f"/domain-types/host/collections/all",
                HostModel,
                list_key="value",
                params={"query": json.dumps(filter), "columns": self._config.host_object_attributes},
            )
        except InvalidInputError:
            return Error(error="Input not allowed.").model_dump()
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()

        return [host.model_dump(exclude_none=True) for host in hosts]

    def _search_hosts_by_folder(self, folder_path: str) -> list[HostModel]:
        return self._client.get(f"/objects/folder_config/{folder_path}/collections/hosts", HostModel, list_key="value")

    def _get_all_hosts(self) -> list[HostModel]:
        return self._client.get(
            "/domain-types/host/collections/all",
            HostModel,
            list_key="value",
            params={"columns": self._config.host_object_attributes},
        )

    def _create_filter(self, filters: dict[str, str]) -> dict:
        return {
            "op": "and",
            "expr": [{"op": "~", "left": col, "right": val} for col, val in filters.items()],
        }
