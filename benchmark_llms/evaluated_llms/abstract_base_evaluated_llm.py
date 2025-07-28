# File: benchmark_llms/abstract_base_evaluated_llm.py

from abc import ABC
import abc
from typing import Dict, Any
from benchmark_llms.evaluated_llms.interface_evaluated_llm import InterfaceEvaluatedLLM
import config.keys_evaluated_llms as config_keys_evaluated_llms
import config.paths
import yaml
import json
import datetime
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager
from benchmark_llms.utils.prompt_helpers import get_deviation_section_from_db

class AbstractBaseEvaluatedLLM(InterfaceEvaluatedLLM, ABC):
    """
    Abstract base class for all concrete LLMs.
    Handles prompt config loading, model overrides, and shared setup logic.
    """

    def __init__(self, model_config: Dict[str, Any]):
        """
        Initialize the LLM with a static config loaded from YAML.
        The config may later be updated with runtime overrides.
        """
        super().__init__(model_config)
        self.prompt_config = {}
        self.system_prompt = ""
        self.user_prompt_prefix = ""
        self.model = None
        self.batch_size = None
        self.temperature = config_keys_evaluated_llms.LLM_TEMPERATURE
        self.max_tokens = config_keys_evaluated_llms.LLM_MAX_TOKENS_DEFAULT
        self.logger = BenchmarkLogFileManager(self.get_model_key())

    def prepare(self, overrides: Dict[str, Any] = None):
        """
        Loads prompt configuration and applies optional runtime overrides.
        Also extracts model and batch size from the resolved config.
        """
        self.prompt_config = self._load_prompt_config()
        self.system_prompt = self.prompt_config.get(config_keys_evaluated_llms.SYSTEM_PROMPT, "")
        self.user_prompt_prefix = self.prompt_config.get(config_keys_evaluated_llms.USER_PROMPT, "")

        deviation_section = get_deviation_section_from_db()
        self.user_prompt_prefix = self.user_prompt_prefix.replace("{{DEVIATION_SECTION}}", deviation_section)

        # Append current UTC time to prompt (for 'future_date' logic)
        current_utc = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        self.user_prompt_prefix += (
            f"\n\nNote: The current timestamp is {current_utc}. All timestamps are in UTC."
        )

        if overrides:
            self.model_config.update(overrides)

        self.model = self.model_config[config_keys_evaluated_llms.MODEL]
        self.batch_size = self.model_config.get(config_keys_evaluated_llms.BATCH_SIZE, config_keys_evaluated_llms.LLM_DEFAULT_BATCH_SIZE)

    def log_input_records(self, records: list[dict]) -> None:
        self.logger.write_log("input_records", {"records": records})

    def log_raw_response(self, raw_output: str) -> None:
        self.logger.write_log("response", raw_output)

    def log_prompt_sent(self, records: list[dict]) -> None:
        self.logger.write_log("prompts_sent", {
            "system_prompt": self.system_prompt,
            "user_prompt": self.build_full_prompt(records)
        })

    @classmethod
    def get_model_key(cls) -> str:
        if not hasattr(cls, "ModelKey") or not cls.ModelKey:
            raise ValueError(f"{cls.__name__} must define a static 'ModelKey'.")
        return cls.ModelKey

    @staticmethod
    def _load_prompt_config(path: str = config.paths.PATH_CONFIG_PROMPT) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def build_prompt(self, record: Dict) -> str:
        return f"{self.user_prompt_prefix}\n{json.dumps(record['content'])}"

    def build_full_prompt(self, record: Any, context_prefix: str = "") -> str:
        return (
            f"{self.user_prompt_prefix}\n\n"
            "Recipe data:\n"
            f"{json.dumps(record, indent=2, sort_keys=True)}"
        )

    def get_prompts(self) -> Dict[str, str]:
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt_prefix
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} model={self.model}>"

    def evaluate(self, records: list[dict]) -> dict:
        self.logger.write_prompt_text_files(self.system_prompt, self.user_prompt_prefix)

        all_deviations = []
        batches = self._split_into_batches(records, batch_size=self.batch_size)

        for i, batch in enumerate(batches, 1):
            self.logger.write_log(f"batch_{i:02d}_input", {"records": batch})
            raw_output = self._run_model_inference(batch)
            self.logger.write_log(f"batch_{i:02d}_response", raw_output)

            parsed = self.parse_model_response(raw_output)
            all_deviations.extend(parsed.get("records", []))

        return {
            "summary_text": f"Consolidated from {len(records)} input records in {len(batches)} batches.",
            "data_quality_score": -1,  # Placeholder until proper scoring
            "records": all_deviations,
        }

    def _split_into_batches(self, records: list[dict], batch_size: int) -> list[list[dict]]:
        return [records[i:i + batch_size] for i in range(0, len(records), batch_size)]

    @abc.abstractmethod
    def _run_model_inference(self, records: list[dict]) -> str:
        """
        Subclasses must implement the actual LLM API call and return the raw string output.
        """
        pass
