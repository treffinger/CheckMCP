from pydantic import AliasPath, Field

from .checkable_object import CheckableObject
from .types import Bool, ServiceState, TimeString


class Service(CheckableObject):
    id: str
    title: str
    description: str | None = Field(validation_alias=AliasPath("extensions", "description"), default=None)
    cache_interval: int | None = Field(validation_alias=AliasPath("extensions", "cache_interval"), default=None)
    cached_at: TimeString | None = Field(validation_alias=AliasPath("extensions", "cached_at"), default=None)
    state: ServiceState | None = Field(validation_alias=AliasPath("extensions", "state"), default=None)
    last_state: ServiceState | None = Field(validation_alias=AliasPath("extensions", "last_state"), default=None)
    hard_state: ServiceState | None = Field(validation_alias=AliasPath("extensions", "hard_state"), default=None)
    last_hard_state: ServiceState | None = Field(
        validation_alias=AliasPath("extensions", "last_hard_state"), default=None
    )
    previous_hard_state: ServiceState | None = Field(
        validation_alias=AliasPath("extensions", "previous_hard_state"), default=None
    )
    in_passive_check_period: Bool | None = Field(
        validation_alias=AliasPath("extensions", "in_passive_check_period"), default=None
    )
    last_time_critical: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "last_time_critical"), default=None
    )
    last_time_ok: TimeString | None = Field(validation_alias=AliasPath("extensions", "last_time_ok"), default=None)
    last_time_unknown: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "last_time_unknown"), default=None
    )
    last_time_warning: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "last_time_warning"), default=None
    )
    obsess_over_service: Bool | None = Field(
        validation_alias=AliasPath("extensions", "obsess_over_service"), default=None
    )
    passive_check_period: str | None = Field(
        validation_alias=AliasPath("extensions", "passive_check_period"), default=None
    )
    tags: dict | None = Field(validation_alias=AliasPath("extensions", "tags"), default=None)
