# File: benchmark_llms/evaluated_llm_openai_gpt_4o.py

from benchmark_llms.evaluated_llms.abstract_implementations.abstract_evaluated_llm_openai import AbstractEvaluatedLLMOpenAI

import config.keys_evaluated_llms as config_keys_evaluated_llms


class EvaluatedLLMOpenAIGPT4o(AbstractEvaluatedLLMOpenAI):
    """
    Concrete implementation for OpenAI's GPT models.
    Uses the shared AbstractEvaluatedLLMProprietary base for config, API key loading, and response parsing.
    """

    ModelKey = config_keys_evaluated_llms.OPENAI_GPT_4O

