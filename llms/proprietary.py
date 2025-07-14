# File: llms/proprietary.py

import os
from llms.base import BaseLLM
from config.keys import API_KEY_ENV

class ProprietaryLLM(BaseLLM):
    """
    Abstract base class for proprietary (closed-source) LLMs.
    Handles shared setup logic like loading API keys.
    Inherits prompt configuration, model selection, and override handling from BaseLLM.
    """

    def prepare(self, overrides=None):
        """
        Calls BaseLLM.prepare() to apply prompt config and runtime overrides,
        then loads the required API key from the specified environment variable.
        """
        super().prepare(overrides=overrides)

        # Load API key from environment
        api_key_env = self.model_config.get(API_KEY_ENV)
        if not api_key_env:
            raise ValueError(f"Missing '{API_KEY_ENV}' in model config for proprietary model.")

        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"Environment variable '{api_key_env}' not set.")