# File: benchmark_llms/evaluated_llms/implementations/evaluated_llm_gemini_1_5_flash.py

from benchmark_llms.evaluated_llms.abstract_implementations.abstract_evaluated_llm_gemini import AbstractEvaluatedLLM_Gemini
import config.keys_evaluated_llms as config_keys
import config.paths as config_paths


class EvaluatedLLM_Gemini1_5Flash(AbstractEvaluatedLLM_Gemini):
    """
    Gemini 1.5 Pro model via google-generativeai SDK.
    Uses shared prompt config and evaluation logic from the benchmark system.
    """

    ModelKey = config_keys.GEMINI_1_5_FLASH

