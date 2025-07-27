# File: benchmark/model_openai.py

import openai
from typing import List, Dict

import benchmark.config.paths
from benchmark.evaluated_llms.abstract_proprietary_evaluated_llm import ProprietaryEvaluatedLLM
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager
import benchmark.config.keys

class OpenAIModel(ProprietaryEvaluatedLLM):
    """
    Concrete implementation for OpenAI's GPT models.
    Uses the shared ProprietaryEvaluatedLLM base for config, API key loading, and response parsing.
    """

    ModelKey = benchmark.config.keys.OPENAI_GPT_4O

    def __init__(self):
        super().__init__(benchmark.config.paths.PATH_CONFIG_OPENAI)
        self.logger = BenchmarkLogFileManager(self.get_model_key())  # Instantiate once

    def evaluate(self, records: List[Dict]) -> Dict:
        self.prepare()

        client = openai.OpenAI(api_key=self.api_key)

        user_prompt = self.build_full_prompt(records)
        system_prompt = self.system_prompt

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        raw_content = response.choices[0].message.content or ""
        content = raw_content.strip()

        self.logger.write_log(suffix="response", content=content)  # Use the instance logger

        return self.parse_model_response(content)