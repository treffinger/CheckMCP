from .request_error import RequestError


class ResourceNotFoundError(RequestError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
