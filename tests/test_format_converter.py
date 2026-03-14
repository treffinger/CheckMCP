import unittest

from format_converter import FormatConverter


class TestFormatConverter(unittest.TestCase):
    def test_slash_is_converted_to_tilde(self):
        result = FormatConverter.normalize_folder_path("/")
        self.assertEqual(result, "~")

    def test_tilde_prefix_added_when_missing(self):
        result = FormatConverter.normalize_folder_path("linux")
        self.assertEqual(result, "~linux")

    def test_tilde_prefix_not_duplicated_when_present(self):
        result = FormatConverter.normalize_folder_path("~linux")
        self.assertEqual(result, "~linux")

    def test_nested_path_with_slashes_converted(self):
        result = FormatConverter.normalize_folder_path("/linux/servers")
        self.assertEqual(result, "~linux~servers")

    def test_nested_path_without_leading_slash(self):
        result = FormatConverter.normalize_folder_path("linux/servers")
        self.assertEqual(result, "~linux~servers")

    def test_already_normalized_path_unchanged(self):
        result = FormatConverter.normalize_folder_path("~linux~servers")
        self.assertEqual(result, "~linux~servers")

    def test_empty_string_gets_tilde_prefix(self):
        result = FormatConverter.normalize_folder_path("")
        self.assertEqual(result, "~")


if __name__ == "__main__":
    unittest.main()
