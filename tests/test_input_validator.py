import unittest

from input_validator import InputValidator
from input_validator.exceptions import InvalidInputError


class TestValidateHostname(unittest.TestCase):
    def test_valid_hostname_is_accepted(self):
        try:
            InputValidator.validate_hostname("my-host_01.example")
        except InvalidInputError:
            self.fail()

    def test_alphanumeric_hostname_is_accepted(self):
        try:
            InputValidator.validate_hostname("server01")
        except InvalidInputError:
            self.fail()

    def test_all_allowed_special_chars_are_accepted(self):
        try:
            InputValidator.validate_hostname("host.-_name")
        except InvalidInputError:
            self.fail()

    def test_disallowed_char_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_hostname("host<script>")

    def test_space_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_hostname("my host")

    def test_colon_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_hostname("host:name")

    def test_empty_string_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_hostname("")

    def test_input_exceeding_140_chars_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_hostname("a" * 141)

    def test_input_at_exactly_140_chars_is_accepted(self):
        try:
            InputValidator.validate_hostname("a" * 140)
        except InvalidInputError:
            self.fail()


class TestValidateDowntimeId(unittest.TestCase):
    def test_valid_numeric_id_is_accepted(self):
        try:
            InputValidator.validate_downtime_id("123")
        except InvalidInputError:
            self.fail()

    def test_letters_raise_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_downtime_id("abc")

    def test_mixed_letters_and_digits_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_downtime_id("1a2")

    def test_empty_string_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_downtime_id("")

    def test_input_exceeding_10_digits_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_downtime_id("1" * 11)

    def test_input_at_exactly_10_digits_is_accepted(self):
        try:
            InputValidator.validate_downtime_id("1" * 10)
        except InvalidInputError:
            self.fail()

    def test_special_chars_raise_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_downtime_id("1<inject>")


class TestValidateFolderPath(unittest.TestCase):
    def test_valid_path_is_accepted(self):
        try:
            InputValidator.validate_folder_path("/linux/servers")
        except InvalidInputError:
            self.fail()

    def test_all_allowed_special_chars_are_accepted(self):
        try:
            InputValidator.validate_folder_path("path.-_#&/ name")
        except InvalidInputError:
            self.fail()

    def test_disallowed_char_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_folder_path("/linux<inject>/servers")

    def test_semicolon_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_folder_path("/linux;servers")

    def test_empty_string_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_folder_path("")

    def test_input_exceeding_100_chars_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_folder_path("a" * 101)

    def test_input_at_exactly_100_chars_is_accepted(self):
        try:
            InputValidator.validate_folder_path("a" * 100)
        except InvalidInputError:
            self.fail()


class TestValidateTag(unittest.TestCase):
    def test_valid_tag_is_accepted(self):
        try:
            InputValidator.validate_tag("criticality:prod")
        except InvalidInputError:
            self.fail()

    def test_alphanumeric_tag_is_accepted(self):
        try:
            InputValidator.validate_tag("mytag123")
        except InvalidInputError:
            self.fail()

    def test_colon_is_accepted(self):
        try:
            InputValidator.validate_tag("key:value")
        except InvalidInputError:
            self.fail()

    def test_disallowed_char_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_tag("tag<inject>:value")

    def test_space_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_tag("my tag:value")

    def test_hyphen_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_tag("my-tag:value")

    def test_empty_string_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_tag("")

    def test_input_exceeding_100_chars_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_tag("a" * 101)

    def test_input_at_exactly_100_chars_is_accepted(self):
        try:
            InputValidator.validate_tag("a" * 100)
        except InvalidInputError:
            self.fail()


class TestValidateSearchFilter(unittest.TestCase):
    def test_valid_filter_is_accepted(self):
        try:
            InputValidator.validate_search_filter({"key": "value"})
        except InvalidInputError:
            self.fail()

    def test_special_chars_in_key_are_accepted(self):
        try:
            InputValidator.validate_search_filter({"key_123": "value"})
        except InvalidInputError:
            self.fail()

    def test_special_chars_in_value_are_accepted(self):
        try:
            InputValidator.validate_search_filter({"key": r"123.-_*\ "})
        except InvalidInputError:
            self.fail()

    def test_disallowed_char_in_key_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_search_filter({"key": "value!"})

    def test_disallowed_char_in_value_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_search_filter({"key!": "value"})

    def test_empty_key_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_search_filter({"key": ""})

    def test_empty_value_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_search_filter({"": "value"})

    def test_key_exceeding_50_chars_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_search_filter({"a" * 51: "value"})

    def test_key_at_exactly_50_chars_is_accepted(self):
        try:
            InputValidator.validate_search_filter({"a" * 50: "value"})
        except InvalidInputError:
            self.fail()

    def test_value_exceeding_200_chars_raises_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_search_filter({"key": "a" * 201})

    def test_value_at_exactly_200_chars_is_accepted(self):
        try:
            InputValidator.validate_search_filter({"key": "a" * 200})
        except InvalidInputError:
            self.fail()

    def test_empty_filter_invalid_input_error(self):
        with self.assertRaises(InvalidInputError):
            InputValidator.validate_search_filter({})


if __name__ == "__main__":
    unittest.main()
