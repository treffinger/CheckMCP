import json
from functools import partial
from pathlib import Path

from pydantic import AliasPath, AnyHttpUrl, BaseModel, Field, model_validator


def load_defaults(key: str) -> set[str]:
    defaults_path = Path(__file__).parent.resolve() / "defaults.json"
    with defaults_path.open() as f:
        defaults: dict[str, list[str]] = json.load(f)
        return set(defaults[key])


class Config(BaseModel):
    cmk_username: str = Field(validation_alias=AliasPath("checkmk", "username"))
    cmk_password: str = Field(validation_alias=AliasPath("checkmk", "password"))
    cmk_url: AnyHttpUrl = Field(validation_alias=AliasPath("checkmk", "url"))
    cmk_site: str = Field(validation_alias=AliasPath("checkmk", "site"))
    auth_mode: str = Field(validation_alias=AliasPath("auth", "mode"))
    issuer_url: AnyHttpUrl | None = Field(validation_alias=AliasPath("auth", "issuer_url"), default=None)
    jwks_url: AnyHttpUrl | None = Field(validation_alias=AliasPath("auth", "jwks_url"), default=None)
    audience: str | None = Field(validation_alias=AliasPath("auth", "audience"), default=None)
    required_scopes: list[str] = Field(validation_alias=AliasPath("auth", "required_scopes"), default=[])
    resource_server_url: AnyHttpUrl | None = Field(
        validation_alias=AliasPath("auth", "resource_server_url"), default=None
    )
    host_object_attributes: set[str] = Field(
        validation_alias=AliasPath("object_attributes", "host"), default_factory=partial(load_defaults, "host")
    )
    service_object_attributes: set[str] = Field(
        validation_alias=AliasPath("object_attributes", "service"), default_factory=partial(load_defaults, "service")
    )
    downtime_object_attributes: set[str] = Field(
        validation_alias=AliasPath("object_attributes", "downtime"), default_factory=partial(load_defaults, "downtime")
    )

    @model_validator(mode="after")
    def check_fields(self):
        allowed_auth_modes = ["none", "oauth"]
        if self.auth_mode not in allowed_auth_modes:
            raise ValueError(
                f"An unknown authentication mode was configured: {self.auth_mode} Allowed authentication modes: {', '.join(allowed_auth_modes)}"
            )

        if self.auth_mode == "oauth" and (
            not self.issuer_url
            or not self.jwks_url
            or not self.resource_server_url
            or not self.required_scopes
            or not self.audience
        ):
            raise ValueError(
                'Invalid configuration. authmode "oauth" has been configured, but one or more of the following values is not set:'
                "issuer_url, jwks_url, resource_server_url, required_scopes, audience"
            )
        return self
