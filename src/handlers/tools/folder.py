from mcp.server.fastmcp import FastMCP

from cmk_client.exceptions import RequestError
from models import Error
from models import Folder as FolderModel

from ..handler import Handler


class Folder(Handler):
    def __init__(self, mcp: FastMCP) -> None:
        super().__init__()
        mcp.tool(description="Lists all Folders")(self.list_folders)

    def list_folders(self) -> list[dict] | dict:
        try:
            folders: list[FolderModel] = self._client.get(
                "/domain-types/folder_config/collections/all",
                FolderModel,
                list_key="value",
                params={"recursive": "true"},
            )
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()
        return [folder.model_dump() for folder in folders]
