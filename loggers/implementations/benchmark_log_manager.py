# File: loggers/implementations/benchmark_log_manager.py

import json
from loggers.abstract_log_file_manager import AbstractLogFileManager
import typing

class BenchmarkLogFileManager(AbstractLogFileManager):
    def __init__(self, model_name: str):
        super().__init__(context_folder="benchmark_llms", subfolder_name=model_name)

    def format_log_content(self, content: typing.Any) -> str:
        if isinstance(content, str):
            try:
                # It's a raw JSON string? Pretty-print it
                return json.dumps(json.loads(content), indent=2)
            except Exception:
                # Not valid JSON? Return as-is
                return content
        return json.dumps(content, indent=2)

    def get_extension(self) -> str:
        return ".json"