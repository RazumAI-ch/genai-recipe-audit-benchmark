# File: loggers/implementations/unit_test_log_manager.py

from loggers.abstract_log_file_manager import AbstractLogFileManager
import config.paths as config_paths

class BenchmarkUnitTestLogFileManager(AbstractLogFileManager):
    def __init__(self):
        super().__init__(context_folder_path=config_paths.PATH_LOGS_UNIT_TESTS, subfolder_name="core")

    def format_log_content(self, content) -> str:
        return str(content)

