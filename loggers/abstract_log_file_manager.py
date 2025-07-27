# File: loggers/abstract_log_file_manager.py

import os
import datetime
import zoneinfo
import typing
import abc
import json


class AbstractLogFileManager(abc.ABC):
    """
    Abstract base class for managing log file creation and storage.
    Subclasses must define the `LOG_FOLDER_PATH` where logs will be saved.
    """

    LOG_FOLDER_PATH: str  # Must be overridden in subclasses

    @classmethod
    def create_timestamp(cls) -> str:
        """
        Generate a CET/CEST timestamp string for filenames.
        """
        cet_now = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Zurich"))
        return cet_now.strftime("%Y-%m-%d_%H-%M-%S")

    @classmethod
    def ensure_log_dir(cls) -> None:
        os.makedirs(cls.LOG_FOLDER_PATH, exist_ok=True)

    @classmethod
    def delete_old_logs(cls) -> None:
        for fname in os.listdir(cls.LOG_FOLDER_PATH):
            file_path = os.path.join(cls.LOG_FOLDER_PATH, fname)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Could not delete file: {file_path} - {e}")

    @classmethod
    def write_log(cls, model_name: str, suffix: str, content: typing.Union[str, dict]) -> str:
        """
        Write log content to a timestamped file in the log folder.
        Format: <timestamp>_<model_name>_<suffix>.json
        """
        cls.ensure_log_dir()
        timestamp = cls.create_timestamp()
        filename = f"{cls.LOG_FOLDER_PATH}/{timestamp}_{model_name}_{suffix}.json"

        with open(filename, "w", encoding="utf-8") as f:
            if isinstance(content, dict):
                json.dump(content, f, indent=2)
            else:
                f.write(str(content))

        return filename