from unittest.mock import MagicMock


HANDLER_CLIENT = "handlers.handler.CmkClient"
HANDLER_CONFIG = "handlers.handler.ConfigLoader"


def make_mock_config():
    config = MagicMock()
    config.cmk_site = "mysite"
    config.host_object_attributes = {"state", "alias"}
    config.service_object_attributes = {"state", "description"}
    config.downtime_object_attributes = {"id", "title", "host_name"}
    return config


def make_mock_mcp():
    mock_mcp = MagicMock()
    mock_mcp.tool.return_value = lambda fn: fn
    return mock_mcp
