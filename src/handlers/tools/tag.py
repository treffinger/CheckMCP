from mcp.server.fastmcp import FastMCP

from cmk_client.exceptions import RequestError
from models import Error
from models import HostTagGroup

from ..handler import Handler


class Tag(Handler):
    def __init__(self, mcp: FastMCP) -> None:
        super().__init__()
        mcp.tool(description="Lists all Tags")(self.list_tags)

    def list_tags(self) -> list[dict] | dict:
        try:
            groups: list[HostTagGroup] = self._client.get(
                "/domain-types/host_tag_group/collections/all", HostTagGroup, list_key="value"
            )
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()
        return [group.model_dump() for group in groups]
