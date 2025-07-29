# File: loggers/implementations/unit_test_log_manager.py

from loggers.abstract_log_file_manager import AbstractLogFileManager
import config.paths as config_paths


class UnitTestLogFileManager(AbstractLogFileManager):
    """
    Generic log file manager for unit tests.

    This class uses the shared ephemeral unit test log path (PATH_LOGS_UNIT_TESTS) and
    allows specifying a custom subfolder name to group logs by test domain (e.g., 'core',
    'db', 'benchmark_unit_tests', 'training_unit_tests'). This avoids over-specializing
    into separate loggers for each test category while still supporting clear separation
    of outputs.

    The default subfolder is 'default', which is used if specific folder is not provided.

    Optionally, a custom context folder path (e.g., PATH_LOGS_ARCHIVABLE) can be provided.
    """

    def __init__(
        self,
        context_folder_path: str = config_paths.PATH_LOGS_UNIT_TESTS,
        subfolder_name: str = "default"
    ):
        super().__init__(
            context_folder_path=context_folder_path,
            subfolder_name=subfolder_name
        )

    def format_log_content(self, content) -> str:
        return str(content)