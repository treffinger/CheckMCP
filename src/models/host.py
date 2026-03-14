from pydantic import AliasPath, Field

from .checkable_object import CheckableObject
from .types import HostState, TimeString


class Host(CheckableObject):
    name: str = Field(validation_alias="id")
    ip_address: str | None = Field(validation_alias=AliasPath("extensions", "address"), default=None)
    alias: str | None = Field(validation_alias=AliasPath("extensions", "alias"), default=None)
    childs: list[str] | None = Field(validation_alias=AliasPath("extensions", "childs"), default=None)
    state: HostState | None = Field(validation_alias=AliasPath("extensions", "state"), default=None)
    last_state: HostState | None = Field(validation_alias=AliasPath("extensions", "last_state"), default=None)
    hard_state: HostState | None = Field(validation_alias=AliasPath("extensions", "hard_state"), default=None)
    last_hard_state: HostState | None = Field(validation_alias=AliasPath("extensions", "last_hard_state"), default=None)
    previous_hard_state: HostState | None = Field(
        validation_alias=AliasPath("extensions", "previous_hard_state"), default=None
    )
    last_time_down: TimeString | None = Field(validation_alias=AliasPath("extensions", "last_time_down"), default=None)
    last_time_unreachable: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "last_time_unreachable"), default=None
    )
    last_time_up: TimeString | None = Field(validation_alias=AliasPath("extensions", "last_time_up"), default=None)
    number_services: int | None = Field(validation_alias=AliasPath("extensions", "num_services"), default=None)
    number_services_warn: int | None = Field(
        validation_alias=AliasPath("extensions", "num_services_warn"), default=None
    )
    number_services_critical: int | None = Field(
        validation_alias=AliasPath("extensions", "num_services_crit"), default=None
    )
