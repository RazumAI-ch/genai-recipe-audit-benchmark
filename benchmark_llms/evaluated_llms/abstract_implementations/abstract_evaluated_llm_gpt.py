# File: benchmark_llms/evaluated_llms/abstract_implementations/abstract_evaluated_llm_gpt.py

import openai
from abc import ABC

from benchmark_llms.evaluated_llms.abstract_evaluated_llm_proprietary import AbstractEvaluatedLLMProprietary
from config import paths as config_paths


class AbstractEvaluatedLLM_GPT(AbstractEvaluatedLLMProprietary, ABC):
    """
    Abstract base class for all OpenAI models (e.g., GPT-4o, GPT-4 Turbo, GPT-3.5).
    Handles OpenAI-specific inference logic using the `gpt` SDK.
    """

    def _run_model_inference(self, records: list[dict]) -> str:
        client = openai.OpenAI(api_key=self.api_key)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.build_full_prompt(records)},
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return (response.choices[0].message.content or "").strip()