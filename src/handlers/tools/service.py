from mcp.server.fastmcp import FastMCP

from cmk_client.exceptions import RequestError, ResourceNotFoundError
from input_validator import InputValidator
from input_validator.exceptions import InvalidInputError
from models import Error
from models import Service as ServiceModel

from ..handler import Handler


class Service(Handler):
    def __init__(self, mcp: FastMCP) -> None:
        super().__init__()
        mcp.tool(description="Returns all services of a Host")(self.get_host_services)

    def get_host_services(self, hostname: str) -> list[dict] | dict:
        try:
            InputValidator.validate_hostname(hostname)
            services: list[ServiceModel] = self._client.get(
                f"/objects/host/{hostname}/collections/services",
                ServiceModel,
                list_key="value",
                params={"columns": self._config.service_object_attributes},
            )
        except InvalidInputError:
            return Error(error="Input not allowed.").model_dump()
        except ResourceNotFoundError:
            return Error(error="Host not found.").model_dump()
        except RequestError:
            return Error(error="An internal Server Error occurred.").model_dump()

        return [service.model_dump(exclude_none=True) for service in services]
