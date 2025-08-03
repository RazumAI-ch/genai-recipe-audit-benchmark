# File: benchmark_llms/evaluated_llms/implementations/evaluated_llm_gemini_1_5_pro.py

from benchmark_llms.evaluated_llms.abstract_implementations.abstract_evaluated_llm_gemini import AbstractEvaluatedLLMGemini
import config.keys_evaluated_llms as config_keys
import config.paths as config_paths


class EvaluatedLLMGemini1_5Pro(AbstractEvaluatedLLMGemini):
    """
    Gemini 1.5 Pro model via google-generativeai SDK.
    Uses shared prompt config and evaluation logic from the benchmark system.
    """

    ModelKey = config_keys.GEMINI_1_5_PRO

    def __init__(self):
        super().__init__(config_paths.PATH_CONFIG_EVALUATED_LLM_GEMINI_1_5_PRO)
