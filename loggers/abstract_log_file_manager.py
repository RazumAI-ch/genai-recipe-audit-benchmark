# File: loggers/abstract_log_file_manager.py

import os
import datetime
import zoneinfo
import typing
import abc
import json
import benchmark_llms.config.paths


class AbstractLogFileManager(abc.ABC):
    """
    Abstract base class for managing log file creation and storage.
    Subclasses must call prepare(model_name) before writing logs.
    """

    LOG_FOLDER_PATH: str = None  # Full resolved path (e.g., logs/ephemeral/debug/benchmark_llms/gpt-4o)
    _context_folder: str = None  # e.g., 'benchmark_llms', 'training'
    _model_subfolder: str = None  # e.g., 'gpt-4o'

    def __init__(self, context_folder: str, subfolder_name: str):
        if not subfolder_name:
            raise ValueError("subfolder_name (typically model name) must be provided.")
        if not context_folder:
            raise ValueError("context_folder (e.g., 'benchmark_llms') must be provided.")

        self._context_folder = context_folder
        self._model_subfolder = subfolder_name
        self.LOG_FOLDER_PATH = os.path.join(
            benchmark_llms.config.paths.PATH_LOGS_DEBUG,
            self._context_folder,
            self._model_subfolder
        )
        self.ensure_log_dir()
        self.delete_old_logs()

    def create_timestamp(self) -> str:
        cet_now = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Zurich"))
        return cet_now.strftime("%Y-%m-%d_%H-%M-%S")

    def ensure_log_dir(self) -> None:
        os.makedirs(self.LOG_FOLDER_PATH, exist_ok=True)

    def delete_old_logs(self) -> None:
        """
        Deletes all but the 5 most recently modified log files in the log folder.
        """
        try:
            files = [
                f for f in os.listdir(self.LOG_FOLDER_PATH)
                if os.path.isfile(os.path.join(self.LOG_FOLDER_PATH, f))
            ]
            files_sorted = sorted(
                files,
                key=lambda f: os.path.getmtime(os.path.join(self.LOG_FOLDER_PATH, f)),
                reverse=True
            )
            for f in files_sorted[5:]:
                try:
                    os.remove(os.path.join(self.LOG_FOLDER_PATH, f))
                except Exception as e:
                    print(f"[WARN] Could not delete file: {f} - {e}")
        except Exception as outer_e:
            print(f"[ERROR] Could not list or process log folder: {self.LOG_FOLDER_PATH} - {outer_e}")

    def write_log(self, suffix: str, content: typing.Union[str, dict]) -> str:
        """
        Write log content to a timestamped file in the log folder.
        Format: <timestamp>_<model_name>_<suffix>.json
        """
        self.ensure_log_dir()
        timestamp = self.create_timestamp()
        filename = os.path.join(self.LOG_FOLDER_PATH, f"{timestamp}_{self._model_subfolder}_{suffix}.json")

        with open(filename, "w", encoding="utf-8") as f:
            if isinstance(content, dict):
                json.dump(content, f, indent=2)
            else:
                f.write(str(content))

        return filename