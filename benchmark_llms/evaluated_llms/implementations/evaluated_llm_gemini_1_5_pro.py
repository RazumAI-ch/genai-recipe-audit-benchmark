# File: benchmark_llms/evaluated_llms/implementations/evaluated_llm_gemini_1_5_pro.py

from google import generativeai as genai
import os

from benchmark_llms.evaluated_llms.abstract_proprietary_evaluated_llm import AbstractProprietaryEvaluatedLLM
import config.keys_evaluated_llms as config_keys
import config.paths as config_paths


class EvaluatedLLMGemini1_5Pro(AbstractProprietaryEvaluatedLLM):
    """
    Gemini 1.5 Pro model via google-generativeai SDK.
    Uses shared prompt config and evaluation logic from the benchmark system.
    """

    ModelKey = config_keys.GEMINI_1_5_PRO

    def __init__(self):
        super().__init__(config_paths.PATH_CONFIG_EVALUATED_LLM_GEMINI_1_5_PRO)

    def prepare(self, overrides=None):
        super().prepare(overrides=overrides)

        api_key = os.getenv(self.model_config.get("api_key_env"))
        if not api_key:
            raise RuntimeError("Environment variable for Gemini API key is not set.")

        genai.configure(api_key=api_key)

    def _run_model_inference(self, records: list[dict]) -> str:
        model = genai.GenerativeModel(self.model)

        prompt = self.build_full_prompt(records)
        response = model.generate_content(prompt)

        return (response.text or "").strip()