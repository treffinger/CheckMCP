import unittest

from pydantic import ValidationError

from config.config import Config


CHECKMK_BASE = {
    "username": "automation",
    "password": "secret",
    "url": "https://checkmk.example.com",
    "site": "mysite",
}


class TestConfigNoneAuth(unittest.TestCase):
    def test_valid_none_auth_config_is_accepted(self):
        data = {"checkmk": CHECKMK_BASE, "auth": {"mode": "none"}}
        config = Config.model_validate(data)
        self.assertEqual(config.cmk_username, "automation")
        self.assertEqual(config.cmk_password, "secret")
        self.assertEqual(config.cmk_site, "mysite")
        self.assertEqual(config.auth_mode, "none")

    def test_none_auth_optional_oauth_fields_are_none(self):
        data = {"checkmk": CHECKMK_BASE, "auth": {"mode": "none"}}
        config = Config.model_validate(data)
        self.assertIsNone(config.issuer_url)
        self.assertIsNone(config.resource_server_url)
        self.assertIsNone(config.audience)
        self.assertEqual(config.required_scopes, [])


class TestConfigOAuthAuth(unittest.TestCase):
    def test_valid_oauth_config_is_accepted(self):
        data = {
            "checkmk": CHECKMK_BASE,
            "auth": {
                "mode": "oauth",
                "issuer_url": "https://auth.example.com",
                "jwks_url": "https://auth.example.com",
                "audience": "audience",
                "resource_server_url": "https://checkmcp.example.com",
                "required_scopes": ["checkmcp:read"],
            },
        }
        config = Config.model_validate(data)
        self.assertIsInstance(config, Config)

    def test_oauth_without_issuer_url_raises(self):
        data = {
            "checkmk": CHECKMK_BASE,
            "auth": {
                "mode": "oauth",
                "resource_server_url": "https://checkmcp.example.com",
                "required_scopes": ["checkmcp:read"],
            },
        }
        with self.assertRaises(ValidationError):
            Config.model_validate(data)

    def test_oauth_without_resource_server_url_raises(self):
        data = {
            "checkmk": CHECKMK_BASE,
            "auth": {
                "mode": "oauth",
                "issuer_url": "https://auth.example.com",
                "required_scopes": ["checkmcp:read"],
            },
        }
        with self.assertRaises(ValidationError):
            Config.model_validate(data)

    def test_oauth_without_required_scopes_raises(self):
        data = {
            "checkmk": CHECKMK_BASE,
            "auth": {
                "mode": "oauth",
                "issuer_url": "https://auth.example.com",
                "resource_server_url": "https://checkmcp.example.com",
                "required_scopes": [],
            },
        }
        with self.assertRaises(ValidationError):
            Config.model_validate(data)


class TestConfigValidation(unittest.TestCase):
    def test_unknown_auth_mode_raises(self):
        data = {"checkmk": CHECKMK_BASE, "auth": {"mode": "basic"}}
        with self.assertRaises(ValidationError) as ctx:
            Config.model_validate(data)
        self.assertIn("unknown authentication mode", str(ctx.exception))

    def test_invalid_url_raises(self):
        data = {
            "checkmk": {**CHECKMK_BASE, "url": "not-a-url"},
            "auth": {"mode": "none"},
        }
        with self.assertRaises(ValidationError):
            Config.model_validate(data)

    def test_missing_checkmk_username_raises(self):
        data = {
            "checkmk": {
                "password": "secret",
                "url": "https://checkmk.example.com",
                "site": "mysite",
            },
            "auth": {"mode": "none"},
        }
        with self.assertRaises(ValidationError):
            Config.model_validate(data)


class TestConfigDefaultObjectAttributes(unittest.TestCase):
    def test_host_attributes_are_loaded_from_defaults(self):
        data = {"checkmk": CHECKMK_BASE, "auth": {"mode": "none"}}
        config = Config.model_validate(data)
        self.assertIsInstance(config.host_object_attributes, set)
        self.assertGreater(len(config.host_object_attributes), 0)

    def test_service_attributes_are_loaded_from_defaults(self):
        data = {"checkmk": CHECKMK_BASE, "auth": {"mode": "none"}}
        config = Config.model_validate(data)
        self.assertIsInstance(config.service_object_attributes, set)
        self.assertGreater(len(config.service_object_attributes), 0)

    def test_downtime_attributes_are_loaded_from_defaults(self):
        data = {"checkmk": CHECKMK_BASE, "auth": {"mode": "none"}}
        config = Config.model_validate(data)
        self.assertIsInstance(config.downtime_object_attributes, set)

    def test_custom_host_attributes_override_defaults(self):
        data = {
            "checkmk": CHECKMK_BASE,
            "auth": {"mode": "none"},
            "object_attributes": {"host": ["alias", "state"]},
        }
        config = Config.model_validate(data)
        self.assertEqual(config.host_object_attributes, {"alias", "state"})


if __name__ == "__main__":
    unittest.main()
