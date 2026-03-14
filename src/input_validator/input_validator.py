import re

from .exceptions import InvalidInputError


class InputValidator:
    @staticmethod
    def validate_hostname(value: str) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9.\-_]{1,140}", value):
            raise InvalidInputError

    @staticmethod
    def validate_downtime_id(value: str) -> None:
        if not re.fullmatch(r"\d{1,10}", value):
            raise InvalidInputError

    @staticmethod
    def validate_folder_path(value: str) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9.\-_#&/ ]{1,100}", value):
            raise InvalidInputError

    @staticmethod
    def validate_tag(value: str) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9:]{1,100}", value):
            raise InvalidInputError

    @staticmethod
    def validate_search_filter(filter: dict[str, str]) -> None:
        if len(filter) == 0:
            raise InvalidInputError

        for key, value in filter.items():
            if not re.fullmatch(r"[a-zA-Z0-9_]{1,50}", key):
                raise InvalidInputError
            if not re.fullmatch(r"[a-zA-Z0-9._\-\*\\\s]{1,200}", value):
                raise InvalidInputError
