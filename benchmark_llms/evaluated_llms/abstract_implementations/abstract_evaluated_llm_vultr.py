# File: benchmark_llms/evaluated_llms/abstract_implementations/abstract_evaluated_llm_vultr.py

import requests
from abc import ABC
from benchmark_llms.evaluated_llms.abstract_evaluated_llm_api_access import AbstractEvaluatedLLM_APIAccess


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
