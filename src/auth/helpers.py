from mcp.server.auth.provider import TokenVerifier
from mcp.server.auth.settings import AuthSettings

from config import ConfigLoader

from .oauth import OAuth


def get_auth_settings() -> AuthSettings | None:
    config = ConfigLoader.get_config()
    if config.auth_mode != "oauth":
        return None

    if not config.issuer_url:
        raise ValueError("issuer_url in config is not set.")

    return AuthSettings(
        issuer_url=config.issuer_url,
        resource_server_url=config.resource_server_url,
        required_scopes=config.required_scopes,
    )


def get_token_verifier() -> TokenVerifier | None:
    config = ConfigLoader.get_config()
    match config.auth_mode:
        case "none":
            return None
        case "oauth":
            return OAuth()
        case _:
            raise ValueError(f"An unknown authentication mode was configured: {config.auth_mode}")
