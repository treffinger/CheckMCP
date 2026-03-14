import logging
from time import time
from typing import override

import requests
from authlib.jose import JoseError, JsonWebKey, JsonWebToken, KeySet
from mcp.server.auth.provider import AccessToken, TokenVerifier
from requests.exceptions import RequestException

from config import ConfigLoader


class OAuth(TokenVerifier):
    def __init__(self) -> None:
        self._config = ConfigLoader.get_config()
        self._jwks: KeySet | None = None
        self._last_key_update = 0

    @override
    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            jwks = self._get_jwks()
            jwt = JsonWebToken(["RS256", "ES256"])

            claims = jwt.decode(
                token,
                jwks,
                claims_options={
                    "iss": {"essential": True, "value": str(self._config.issuer_url)},
                    "aud": {"essential": True, "value": self._config.audience},
                    "exp": {"essential": True},
                },
            )
            claims.validate()
        except RequestException as e:
            logging.error(f"JWKS could not be retrieved. Error: {e}")
            return None
        except JoseError:
            return None

        return AccessToken(
            token=token,
            client_id=claims.get("client_id") or claims.get("sub") or "",
            scopes=claims.get("scope", "").split(),
        )

    def _get_jwks(self) -> KeySet:
        delta = time() - self._last_key_update
        if self._jwks is None or delta > 300:
            response = requests.get(str(self._config.jwks_url), timeout=10)
            response.raise_for_status()
            self._jwks = JsonWebKey.import_key_set(response.json())
            self._last_key_update = time()
        return self._jwks
