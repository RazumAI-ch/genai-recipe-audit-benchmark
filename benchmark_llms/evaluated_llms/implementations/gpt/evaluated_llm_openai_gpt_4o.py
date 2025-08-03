# File: benchmark_llms/evaluated_llm_openai_gpt_4o.py

from benchmark_llms.evaluated_llms.abstract_implementations.abstract_evaluated_llm_gpt import AbstractEvaluatedLLM_GPT

import config.keys_evaluated_llms as config_keys_evaluated_llms


class EvaluatedLLM_GPT4o(AbstractEvaluatedLLM_GPT):
    """
    Concrete implementation for OpenAI's GPT models.
    Uses the shared AbstractEvaluatedLLMProprietary base for config, API key loading, and response parsing.
    """

    ModelKey = config_keys_evaluated_llms.GPT_4O

