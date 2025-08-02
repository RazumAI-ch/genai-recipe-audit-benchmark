# File: benchmark_llms/evaluated_llm_openai_gpt_4o.py

import openai

from benchmark_llms.evaluated_llms.abstract_proprietary_evaluated_llm import AbstractProprietaryEvaluatedLLM

import config.keys_evaluated_llms as config_keys_evaluated_llms
import config.paths as config_paths

class EvaluatedLLMOpenAIGPT4o(AbstractProprietaryEvaluatedLLM):
    """
    Concrete implementation for OpenAI's GPT models.
    Uses the shared AbstractProprietaryEvaluatedLLM base for config, API key loading, and response parsing.
    """

    ModelKey = config_keys_evaluated_llms.OPENAI_GPT_4O

    def __init__(self):
        super().__init__(config_paths.PATH_CONFIG_OPENAI_GPT_4o)

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