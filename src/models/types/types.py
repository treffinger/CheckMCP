from datetime import datetime, timezone
from typing import Annotated

from pydantic import BeforeValidator


def convert_to_bool(value: int) -> bool:
    match value:
        case 0:
            return False
        case 1:
            return True
    raise ValueError


def convert_to_acknowledgement_type(value: int) -> str:
    match value:
        case 0:
            return "none"
        case 1:
            return "normal"
        case 2:
            return "sticky"
    raise ValueError


def convert_to_time_string(value: int) -> str:
    if value == 0:
        return "-"
    return str(datetime.fromtimestamp(value, tz=timezone.utc))


def convert_to_check_options(value: int) -> str:
    match value:
        case 0:
            return "forced"
        case 1:
            return "normal"
        case 2:
            return "freshness"
    raise ValueError


def convert_to_check_type(value: int) -> str:
    match value:
        case 0:
            return "active"
        case 1:
            return "passive"
    raise ValueError


def convert_to_service_state(value: int) -> str:
    match value:
        case 0:
            return "ok"
        case 1:
            return "warn"
        case 2:
            return "critical"
        case 3:
            return "unknown"
    raise ValueError


def convert_to_host_state(value: int) -> str:
    match value:
        case 0:
            return "up"
        case 1:
            return "down"
        case 2:
            return "unreachable"

    raise ValueError


def convert_to_state_type(value: int) -> str:
    match value:
        case 0:
            return "soft"
        case 1:
            return "hard"
    raise ValueError


Bool = Annotated[bool, BeforeValidator(convert_to_bool)]
AcknowledgementType = Annotated[str, BeforeValidator(convert_to_acknowledgement_type)]
TimeString = Annotated[str, BeforeValidator(convert_to_time_string)]
CheckOptions = Annotated[str, BeforeValidator(convert_to_check_options)]
CheckType = Annotated[str, BeforeValidator(convert_to_check_type)]
ServiceState = Annotated[str, BeforeValidator(convert_to_service_state)]
HostState = Annotated[str, BeforeValidator(convert_to_host_state)]
StateType = Annotated[str, BeforeValidator(convert_to_state_type)]
