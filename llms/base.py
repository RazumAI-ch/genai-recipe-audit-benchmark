# File: llms/base.py

from abc import ABC
from typing import Dict, Any
from llms.interface import LLMInterface
from config.loader import load_prompt_config


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
        from config/prompts.yaml.
        """
        self.prompt_config = load_prompt_config()
        self.system_prompt = self.prompt_config.get("system_prompt", "")
        self.user_prompt_prefix = self.prompt_config.get("user_prompt_prefix", "")