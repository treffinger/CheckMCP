from pydantic import AliasPath, BaseModel, Field, field_validator

from .types import AcknowledgementType, Bool, CheckOptions, CheckType, StateType, TimeString


class CheckableObject(BaseModel):
    accept_passive_checks: Bool | None = Field(
        validation_alias=AliasPath("extensions", "accept_passive_checks"), default=None
    )
    acknowledged: Bool | None = Field(validation_alias=AliasPath("extensions", "acknowledged"), default=None)
    acknowledgement_type: AcknowledgementType | None = Field(
        validation_alias=AliasPath("extensions", "acknowledgement_type"), default=None
    )
    active_checks_enabled: Bool | None = Field(
        validation_alias=AliasPath("extensions", "active_checks_enabled"), default=None
    )
    check_command: str | None = Field(validation_alias=AliasPath("extensions", "check_command"), default=None)
    check_command_expanded: str | None = Field(
        validation_alias=AliasPath("extensions", "check_command_expanded"), default=None
    )
    check_flapping_recovery_notification: Bool | None = Field(
        validation_alias=AliasPath("extensions", "check_flapping_recovery_notification"), default=None
    )
    check_freshness: Bool | None = Field(validation_alias=AliasPath("extensions", "check_freshness"), default=None)
    check_interval: float | None = Field(validation_alias=AliasPath("extensions", "check_interval"), default=None)
    check_options: CheckOptions | None = Field(validation_alias=AliasPath("extensions", "check_options"), default=None)
    check_period: str | None = Field(validation_alias=AliasPath("extensions", "check_period"), default=None)
    check_type: CheckType | None = Field(validation_alias=AliasPath("extensions", "check_type"), default=None)
    checks_enabled: Bool | None = Field(validation_alias=AliasPath("extensions", "checks_enabled"), default=None)
    comments: list[int] | None = Field(validation_alias=AliasPath("extensions", "comments"), default=None)
    contact_groups: list[str] | None = Field(validation_alias=AliasPath("extensions", "contact_groups"), default=None)
    contacts: list[str] | None = Field(validation_alias=AliasPath("extensions", "contacts"), default=None)
    current_check_attempt: int | None = Field(validation_alias=AliasPath("extensions", "current_attempt"), default=None)
    current_notification_number: int | None = Field(
        validation_alias=AliasPath("extensions", "current_notification_number"), default=None
    )
    custom_variables: dict[str, str] | None = Field(
        validation_alias=AliasPath("extensions", "custom_variables"), default=None
    )
    display_name: str | None = Field(validation_alias=AliasPath("extensions", "display_name"), default=None)
    downtimes: list[int] | None = Field(validation_alias=AliasPath("extensions", "downtimes"), default=None)
    event_handler_command: str | None = Field(validation_alias=AliasPath("extensions", "event_handler"), default=None)
    event_handler_enabled: Bool | None = Field(
        validation_alias=AliasPath("extensions", "event_handler_enabled"), default=None
    )
    check_execution_time: float | None = Field(validation_alias=AliasPath("extensions", "execution_time"), default=None)
    first_notification_delay: float | None = Field(
        validation_alias=AliasPath("extensions", "first_notification_delay"), default=None
    )
    flap_detection_enabled: Bool | None = Field(
        validation_alias=AliasPath("extensions", "flap_detection_enabled"), default=None
    )
    flappiness: float | None = Field(validation_alias=AliasPath("extensions", "flappiness"), default=None)
    groups: list[str] | None = Field(validation_alias=AliasPath("extensions", "groups"), default=None)
    has_been_checked: Bool | None = Field(validation_alias=AliasPath("extensions", "has_been_checked"), default=None)
    high_flap_threshold: float | None = Field(
        validation_alias=AliasPath("extensions", "high_flap_threshold"), default=None
    )
    in_check_period: Bool | None = Field(validation_alias=AliasPath("extensions", "in_check_period"), default=None)
    in_notification_period: Bool | None = Field(
        validation_alias=AliasPath("extensions", "in_notification_period"), default=None
    )
    in_service_period: Bool | None = Field(validation_alias=AliasPath("extensions", "in_service_period"), default=None)
    initial_state: int | None = Field(validation_alias=AliasPath("extensions", "initial_state"), default=None)
    is_executing: Bool | None = Field(validation_alias=AliasPath("extensions", "is_executing"), default=None)
    is_flapping: Bool | None = Field(validation_alias=AliasPath("extensions", "is_flapping"), default=None)
    labels: dict | None = Field(validation_alias=AliasPath("extensions", "labels"), default=None)
    last_check: TimeString | None = Field(validation_alias=AliasPath("extensions", "last_check"), default=None)
    last_hard_state_change: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "last_hard_state_change"), default=None
    )
    last_notification: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "last_notification"), default=None
    )
    last_state_change: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "last_state_change"), default=None
    )
    check_latency: float | None = Field(validation_alias=AliasPath("extensions", "latency"), default=None)
    long_plugin_output: str | None = Field(validation_alias=AliasPath("extensions", "long_plugin_output"), default=None)
    low_flap_threshold: float | None = Field(
        validation_alias=AliasPath("extensions", "low_flap_threshold"), default=None
    )
    max_check_attempts: int | None = Field(validation_alias=AliasPath("extensions", "max_check_attempts"), default=None)
    next_check: TimeString | None = Field(validation_alias=AliasPath("extensions", "next_check"), default=None)
    next_notification: TimeString | None = Field(
        validation_alias=AliasPath("extensions", "next_notification"), default=None
    )
    no_more_notifications: Bool | None = Field(
        validation_alias=AliasPath("extensions", "no_more_notifications"), default=None
    )
    notes: str | None = Field(validation_alias=AliasPath("extensions", "notes"), default=None)
    notification_interval_minutes: int | None = Field(
        validation_alias=AliasPath("extensions", "notification_interval"), default=None
    )
    notification_period: str | None = Field(
        validation_alias=AliasPath("extensions", "notification_period"), default=None
    )
    notification_postponement_reason: str | None = Field(
        validation_alias=AliasPath("extensions", "notification_postponement_reason"), default=None
    )
    notifications_enabled: Bool | None = Field(
        validation_alias=AliasPath("extensions", "notifications_enabled"), default=None
    )
    pending_flex_downtime: int | None = Field(
        validation_alias=AliasPath("extensions", "pending_flex_downtime"), default=None
    )
    percent_state_change: float | None = Field(
        validation_alias=AliasPath("extensions", "percent_state_change"), default=None
    )
    performance_data: str | None = Field(validation_alias=AliasPath("extensions", "perf_data"), default=None)
    plugin_output: str | None = Field(validation_alias=AliasPath("extensions", "plugin_output"), default=None)
    process_performance_data_enabled: Bool | None = Field(
        validation_alias=AliasPath("extensions", "process_performance_data"), default=None
    )
    check_retry_interval: float | None = Field(validation_alias=AliasPath("extensions", "retry_interval"), default=None)
    scheduled_downtime_depth: int | None = Field(
        validation_alias=AliasPath("extensions", "scheduled_downtime_depth"), default=None
    )
    service_period: str | None = Field(validation_alias=AliasPath("extensions", "service_period"), default=None)
    staleness: float | None = Field(validation_alias=AliasPath("extensions", "staleness"), default=None)
    state_type: StateType | None = Field(validation_alias=AliasPath("extensions", "state_type"), default=None)
