# File: benchmark_llms/evaluated_llms/implementations/mistral/evaluated_llm_mistral_7b_instruct.py

from benchmark_llms.evaluated_llms.abstract_implementations.abstract_evaluated_llm_mistral import AbstractEvaluatedLLMMistral
import config.keys_evaluated_llms as config_keys


class EvaluatedLLMMistral7BInstruct(AbstractEvaluatedLLMMistral):
    """
    Mistral 7B Instruct model, currently served via Vultr serverless API.
    Uses standard prompt and evaluation logic.
    """

    ModelKey = config_keys.MISTRAL_7B_INSTRUCT