# File: loggers/implementations/benchmark_log_manager.py

from loggers.abstract_log_file_manager import AbstractLogFileManager

class BenchmarkLogFileManager(AbstractLogFileManager):
    """
    Log manager for benchmark evaluation runs.

    Stores logs under:
        logs/ephemeral/debug/benchmark/<model_name>/
    """

    def __init__(self, model_name: str):
        """
        Initializes the log manager for a specific model's benchmark logs.

        Args:
            model_name (str): Unique identifier of the model (used as subfolder).
        """
        super().__init__(context_folder="benchmark", subfolder_name=model_name)