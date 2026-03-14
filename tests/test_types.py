import unittest

from models.types.types import (
    convert_to_acknowledgement_type,
    convert_to_bool,
    convert_to_check_options,
    convert_to_check_type,
    convert_to_host_state,
    convert_to_service_state,
    convert_to_state_type,
    convert_to_time_string,
)


class TestConvertToBool(unittest.TestCase):
    def test_zero_returns_false(self):
        self.assertIs(convert_to_bool(0), False)

    def test_one_returns_true(self):
        self.assertIs(convert_to_bool(1), True)

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_bool(2)


class TestConvertToServiceState(unittest.TestCase):
    def test_zero_returns_ok(self):
        self.assertEqual(convert_to_service_state(0), "ok")

    def test_one_returns_warn(self):
        self.assertEqual(convert_to_service_state(1), "warn")

    def test_two_returns_critical(self):
        self.assertEqual(convert_to_service_state(2), "critical")

    def test_three_returns_unknown(self):
        self.assertEqual(convert_to_service_state(3), "unknown")

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_service_state(4)


class TestConvertToHostState(unittest.TestCase):
    def test_zero_returns_up(self):
        self.assertEqual(convert_to_host_state(0), "up")

    def test_one_returns_down(self):
        self.assertEqual(convert_to_host_state(1), "down")

    def test_two_returns_unreachable(self):
        self.assertEqual(convert_to_host_state(2), "unreachable")

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_host_state(3)


class TestConvertToStateType(unittest.TestCase):
    def test_zero_returns_soft(self):
        self.assertEqual(convert_to_state_type(0), "soft")

    def test_one_returns_hard(self):
        self.assertEqual(convert_to_state_type(1), "hard")

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_state_type(2)


class TestConvertToCheckType(unittest.TestCase):
    def test_zero_returns_active(self):
        self.assertEqual(convert_to_check_type(0), "active")

    def test_one_returns_passive(self):
        self.assertEqual(convert_to_check_type(1), "passive")

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_check_type(2)


class TestConvertToCheckOptions(unittest.TestCase):
    def test_zero_returns_forced(self):
        self.assertEqual(convert_to_check_options(0), "forced")

    def test_one_returns_normal(self):
        self.assertEqual(convert_to_check_options(1), "normal")

    def test_two_returns_freshness(self):
        self.assertEqual(convert_to_check_options(2), "freshness")

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_check_options(3)


class TestConvertToAcknowledgementType(unittest.TestCase):
    def test_zero_returns_none(self):
        self.assertEqual(convert_to_acknowledgement_type(0), "none")

    def test_one_returns_normal(self):
        self.assertEqual(convert_to_acknowledgement_type(1), "normal")

    def test_two_returns_sticky(self):
        self.assertEqual(convert_to_acknowledgement_type(2), "sticky")

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_acknowledgement_type(3)


class TestConvertToTimeString(unittest.TestCase):
    def test_zero_returns_dash(self):
        self.assertEqual(convert_to_time_string(0), "-")

    def test_valid_timestamp_returns_string(self):
        result = convert_to_time_string(1700000000)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "-")
        self.assertIn("2023", result)

    def test_return_type_is_string(self):
        result = convert_to_time_string(1700000000)
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
