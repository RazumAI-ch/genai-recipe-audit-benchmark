# File: benchmark_llms/evaluated_llms/abstract_implementations/abstract_evaluated_llm_vultr.py

# ==============================================================================
# AbstractEvaluatedLLMVultr
# ------------------------------------------------------------------------------
# This abstract class provides the Vultr-specific implementation for making
# OpenAI-compatible chat completions via Vultr Serverless Inference API.
#
# It inherits API key management from AbstractEvaluatedLLM_APIAccess and focuses
# only on HTTP communication with the Vultr endpoint.
#
# Any model (e.g., Mistral, LLaMA, DeepSeek) that is currently served via Vultr
# should inherit from a provider-agnostic abstract class (e.g., AbstractEvaluatedLLMMistral)
# which in turn inherits from this class.
#
# If we later migrate to a different provider (e.g., TogetherAI), only the
# intermediate abstract class needs to change—not each individual model file.
# ==============================================================================

import requests
from abc import ABC
from benchmark_llms.deprecated.evaluated_llms.abstract_evaluated_llm_api_access import AbstractEvaluatedLLM_APIAccess


class AbstractEvaluatedLLMVultr(AbstractEvaluatedLLM_APIAccess, ABC):
    """
    Abstract base class for models hosted via Vultr Serverless Inference.
    Uses OpenAI-compatible chat API and inherits API key logic from proprietary base.
    """

    def _run_model_inference(self, records: list[dict]) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.build_full_prompt(records)}
        ]

        api_url = f"{self.model_config.get('base_url')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Vultr inference call failed: {e}")