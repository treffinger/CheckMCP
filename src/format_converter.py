class FormatConverter:
    @staticmethod
    def normalize_folder_path(folder_path: str) -> str:
        folder_path = folder_path.replace("/", "~")
        if not folder_path.startswith("~"):
            return f"~{folder_path}"
        return folder_path
