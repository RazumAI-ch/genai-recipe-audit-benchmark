# File: loggers/implementations/training_log_manager.py

from loggers.abstract_log_file_manager import AbstractLogFileManager

class TrainingLogFileManager(AbstractLogFileManager):
    """
    Log manager for training runs.

    Stores logs under:
        archive/logs/ephemeral/debug/training/<model_name>/
    """
    def __init__(self, model_name: str):
        super().__init__(context_folder="training", subfolder_name=model_name)