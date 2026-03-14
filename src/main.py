from mcp.server.fastmcp import FastMCP

from auth import get_auth_settings, get_token_verifier
from handlers.tools import Downtime, Folder, Host, Service, Tag


def register_tools(mcp: FastMCP) -> None:
    Downtime(mcp)
    Folder(mcp)
    Host(mcp)
    Service(mcp)
    Tag(mcp)


mcp = FastMCP(
    "CheckMCP",
    token_verifier=get_token_verifier(),
    auth=get_auth_settings(),
)

register_tools(mcp)

app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run("streamable-http")
