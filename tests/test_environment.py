import os
import unittest
from unittest.mock import patch

from environment.environment import Environment


class TestEnvironment(unittest.TestCase):
    def test_get_existing_variable_returns_value(self):
        with patch.dict(os.environ, {"MY_TEST_VAR": "test"}):
            result = Environment.get_variable("MY_TEST_VAR")
        self.assertEqual(result, "test")

    def test_get_missing_variable_raises_value_error(self):
        env_without_var = {k: v for k, v in os.environ.items() if k != "MY_MISSING_VAR"}
        with patch.dict(os.environ, env_without_var, clear=True):
            with self.assertRaises(ValueError):
                Environment.get_variable("MY_MISSING_VAR")


if __name__ == "__main__":
    unittest.main()
