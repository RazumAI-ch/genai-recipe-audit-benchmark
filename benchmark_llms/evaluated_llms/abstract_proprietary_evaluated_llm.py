# File: benchmark_llms/abstract_proprietary_evaluated_llm.py

import os
from abc import ABC
import json
from benchmark_llms.evaluated_llms.abstract_base_evaluated_llm import AbstractBaseEvaluatedLLM
import benchmark_llms.utils.utils as utils
from config.keys import API_KEY_ENV


class AbstractProprietaryEvaluatedLLM(AbstractBaseEvaluatedLLM, ABC):
    """
    Abstract base class for proprietary (closed-source) LLMs.
    Handles shared setup logic like loading API keys.
    """

    def prepare(self, overrides=None):
        super().prepare(overrides=overrides)

        api_key_env = self.model_config.get(API_KEY_ENV)
        if not api_key_env:
            raise ValueError(f"Missing '{API_KEY_ENV}' in model config for proprietary model.")

        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"Environment variable '{api_key_env}' not set.")

    def parse_model_response(self, content: str) -> dict:
        """
        Shared logic for extracting and validating JSON from raw LLM response.
        Ensures response is well-formed and normalized.
        """
        if not content:
            raise ValueError("Empty response from LLM.")

        try:
            clean_json = utils.extract_json_from_text(content)

            if not clean_json.strip().startswith("{") and not clean_json.strip().startswith("["):
                print(f"Cleaned content starts with: {clean_json.strip()[:60]}")
                raise ValueError("Cleaned response is not valid JSON — check for Markdown formatting or truncation.")

            if '"issue%' in clean_json or clean_json.strip().endswith(","):
                print("Possible truncation detected at end of response.")

            parsed = json.loads(clean_json)

            if isinstance(parsed, list):
                parsed = {
                    "summary_text": "",
                    "records": parsed
                }

            if "summary_text" not in parsed:
                parsed["summary_text"] = ""

            return parsed

        except Exception as e:
            print("LLM returned invalid JSON. Check saved logs.")
            raise ValueError(f"JSON parsing failed: {e}")