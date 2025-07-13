# File: llms/proprietary.py

import os
from llms.base import BaseLLM
from config.keys import API_KEY_ENV, MODEL, BATCH_SIZE

class ProprietaryLLM(BaseLLM):
    """
    Abstract base class for proprietary (closed-source) LLMs.
    Handles shared setup logic like loading API keys, model name, and batch size.
    """

    def prepare(self):
        super().prepare()

        # Load API key from environment
        api_key_env = self.model_config.get(API_KEY_ENV)
        if not api_key_env:
            raise ValueError(f"Missing '{API_KEY_ENV}' in model config for proprietary model.")

        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"Environment variable '{api_key_env}' not set.")

        # Required config parameters
        self.model = self.model_config.get(MODEL)
        if not self.model:
            raise ValueError(f"Missing required config key: '{MODEL}'")

        self.batch_size = self.model_config.get(BATCH_SIZE)
        if self.batch_size is None:
            raise ValueError(f"Missing required config key: '{BATCH_SIZE}'")