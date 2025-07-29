# File: loggers/implementations/benchmark_unit_test_log_manager.py

from loggers.abstract_log_file_manager import AbstractLogFileManager
import config.paths as config_paths

class BenchmarkUnitTestLogFileManager(AbstractLogFileManager):
    def __init__(self):
        super().__init__(context_folder_path=config_paths.PATH_LOGS_EPHEMERAL, subfolder_name="benchmark_unit_tests_logs")

    def format_log_content(self, content) -> str:
        return str(content)

