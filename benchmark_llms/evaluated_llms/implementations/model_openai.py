# File: benchmark_llms/model_openai.py

import openai
from typing import List, Dict

import config.paths
from benchmark_llms.evaluated_llms.abstract_proprietary_evaluated_llm import ProprietaryEvaluatedLLM
import config.keys


class OpenAIModel(ProprietaryEvaluatedLLM):
    """
    Concrete implementation for OpenAI's GPT models.
    Uses the shared ProprietaryEvaluatedLLM base for config, API key loading, and response parsing.
    """

    ModelKey = config.keys.OPENAI_GPT_4O

    def __init__(self):
        super().__init__(config.paths.PATH_CONFIG_OPENAI)

    def _run_model_inference(self, records: list[dict]) -> str:
        import openai
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