# File: llms/base.py

from abc import ABC
from typing import Dict, Any
from llms.interface import LLMInterface
from config.keys import SYSTEM_PROMPT, USER_PROMPT_PREFIX, MODEL, BATCH_SIZE
from config.paths import PROMPT_CONFIG_PATH
import yaml
import json


class BaseLLM(LLMInterface, ABC):
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

    def prepare(self, overrides: Dict[str, Any] = None):
        """
        Loads prompt configuration and applies optional runtime overrides.
        Also extracts model and batch size from the resolved config.

        If overrides are provided, they replace the corresponding entries
        in the original model_config (e.g., to change model version dynamically).
        """
        self.prompt_config = self._load_prompt_config()
        self.system_prompt = self.prompt_config.get(SYSTEM_PROMPT, "")
        self.user_prompt_prefix = self.prompt_config.get(USER_PROMPT_PREFIX, "")

        # Merge in runtime overrides
        if overrides:
            self.model_config.update(overrides)

        # Required fields — fail fast if missing
        self.model = self.model_config[MODEL]
        self.batch_size = self.model_config[BATCH_SIZE]

    def _load_prompt_config(self, path: str = PROMPT_CONFIG_PATH) -> dict:
        """
        Load system and user prompts from the YAML config file.
        Used to provide consistent prompting across models.
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def build_prompt(self, record: Dict) -> str:
        """
        Construct a prompt from the user prompt prefix and JSON-formatted record.

        This can be overridden by subclasses if a model requires
        special formatting, wrapping, or multi-step inputs.
        """
        return f"{self.user_prompt_prefix}\n{json.dumps(record['content'])}"

    def build_full_prompt(self, record: Any, context_prefix: str = "") -> str:
        """
        Construct the full user prompt.

        - If context_prefix is provided (e.g., deviation catalog), it is prepended.
        - Accepts either a single record (dict) or list of records.
        """
        context = context_prefix.strip()
        record_json = json.dumps(record, indent=2)
        base_prompt = f"{self.user_prompt_prefix}\n{record_json}"
        return f"{context}\n\n{base_prompt}" if context else base_prompt

