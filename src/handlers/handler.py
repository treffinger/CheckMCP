from cmk_client import CmkClient
from config import ConfigLoader, Config


class Handler:
    def __init__(self) -> None:
        self._client: CmkClient = CmkClient()
        self._config: Config = ConfigLoader.get_config()
