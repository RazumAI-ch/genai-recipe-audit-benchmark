# File: benchmark_llms/abstract_base_evaluated_llm.py

from abc import ABC
from typing import Dict, Any
from benchmark_llms.evaluated_llms.interface_llm import EvaluatedLLMInterface
import benchmark_llms.config.keys
import benchmark_llms.config.paths
import yaml
import json


class BaseEvaluatedLLM(EvaluatedLLMInterface, ABC):
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
        self.temperature = benchmark_llms.config.keys.LLM_TEMPERATURE
        self.max_tokens = benchmark_llms.config.keys.LLM_MAX_TOKENS_DEFAULT

    def prepare(self, overrides: Dict[str, Any] = None):
        """
        Loads prompt configuration and applies optional runtime overrides.
        Also extracts model and batch size from the resolved config.

        If overrides are provided, they replace the corresponding entries
        in the original model_config (e.g., to change model version dynamically).
        """
        self.prompt_config = self._load_prompt_config()
        self.system_prompt = self.prompt_config.get(benchmark_llms.config.keys.SYSTEM_PROMPT, "")
        self.user_prompt_prefix = self.prompt_config.get(benchmark_llms.config.keys.USER_PROMPT, "")

        # Merge in runtime overrides
        if overrides:
            self.model_config.update(overrides)

        # Required fields — fail fast if missing
        self.model = self.model_config[benchmark_llms.config.keys.MODEL]
        self.batch_size = self.model_config.get(benchmark_llms.config.keys.BATCH_SIZE, 10)

    @classmethod
    def get_model_key(cls) -> str:
        if not hasattr(cls, "ModelKey") or not cls.ModelKey:
            raise ValueError(f"{cls.__name__} must define a static 'ModelKey'.")
        return cls.ModelKey


    @staticmethod
    def _load_prompt_config(path: str = benchmark_llms.config.paths.PATH_CONFIG_PROMPT) -> dict:
        """
        Load system and user prompts from the YAML config file.
        Used to provide consistent prompting across models.
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def build_prompt(self, record: Dict) -> str:
        """
        Construct a prompt from the user prompt prefix and JSON-formatted record.

        Subclasses can override this if a model requires
        special formatting, wrapping, or multistep inputs.
        """
        return f"{self.user_prompt_prefix}\n{json.dumps(record['content'])}"

    def build_full_prompt(self, record: Any, context_prefix: str = "") -> str:
        """
        Construct the full user prompt.

        - Accepts a list of records (preferred usage).
        - Matches the format used by the Streamlit validator:
            <user_prompt_prefix>

            Recipe data:
            <pretty-printed, sorted JSON>
        """
        return (
            f"{self.user_prompt_prefix}\n\n"
            "Recipe data:\n"
            f"{json.dumps(record, indent=2, sort_keys=True)}"
        )

    def get_prompts(self) -> Dict[str, str]:
        """
        Returns both system and user prompt strings.
        Useful for inspection, testing, or logging.
        """
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt_prefix
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} model={self.model}>"