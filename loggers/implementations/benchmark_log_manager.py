# File: loggers/benchmark_log_manager.py

import config.paths
from loggers.abstract_log_file_manager import AbstractLogFileManager


class BenchmarkLogFileManager(AbstractLogFileManager):
    """
    Concrete log manager for benchmark-related logs.
    Inherits timestamp and directory logic from AbstractLogFileManager.
    """
    LOG_FOLDER_PATH = config.paths.PATH_LOGS_DEBUG
