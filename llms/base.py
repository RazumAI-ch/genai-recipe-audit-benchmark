# File: llms/base.py

from abc import ABC
from typing import Dict, Any
from llms.interface import LLMInterface
from config.keys import SYSTEM_PROMPT, USER_PROMPT_PREFIX
from config.paths import PROMPT_CONFIG_PATH
import yaml

class BaseLLM(LLMInterface, ABC):
    """
    Abstract base class for all concrete LLMs.
    Handles prompt config loading and shared setup logic.
    """

    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)
        self.prompt_config = {}
        self.system_prompt = ""
        self.user_prompt_prefix = ""

    def prepare(self):
        """
        Loads the shared system and user prompt configuration
        from the configured prompt file.
        """
        self.prompt_config = self._load_prompt_config()
        self.system_prompt = self.prompt_config.get(SYSTEM_PROMPT, "")
        self.user_prompt_prefix = self.prompt_config.get(USER_PROMPT_PREFIX, "")

    def _load_prompt_config(self, path: str = PROMPT_CONFIG_PATH) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)