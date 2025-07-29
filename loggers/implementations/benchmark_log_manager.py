# File: loggers/implementations/benchmark_log_manager.py

import os
import json
import typing
from loggers.abstract_log_file_manager import AbstractLogFileManager
import config.paths as config_paths

class BenchmarkLogFileManager(AbstractLogFileManager):
    def __init__(self, model_name: str):
        super().__init__(context_folder_path=config_paths.PATH_LOGS_DEBUG, subfolder_name=model_name)

    def get_extension(self) -> str:
        return ".json"

    def format_log_content(self, content: typing.Any) -> str:
        if isinstance(content, dict):
            return json.dumps(content, indent=2)
        return str(content)

    def write_prompt_text_files(self, system_prompt: str, user_prompt: str):
        timestamp = self.create_timestamp()

        system_path = os.path.join(
            self.LOG_FOLDER_PATH, f"{timestamp}_{self._model_subfolder}_system_prompt.txt"
        )
        user_path = os.path.join(
            self.LOG_FOLDER_PATH, f"{timestamp}_{self._model_subfolder}_user_prompt.txt"
        )

        with open(system_path, "w", encoding="utf-8") as f_sys:
            f_sys.write(system_prompt)

        with open(user_path, "w", encoding="utf-8") as f_usr:
            f_usr.write(user_prompt)