# abstract_evaluated_llm_gemini.py
import os
from abc import ABC, abstractmethod
from google import generativeai as genai

from benchmark_llms.evaluated_llms.abstract_evaluated_llm_proprietary import AbstractEvaluatedLLMProprietary

class AbstractEvaluatedLLM_Gemini(AbstractEvaluatedLLMProprietary, ABC):
    """
    Abstract base for all Gemini-evaluated LLMs (e.g., Gemini 1.5 Pro, Gemini 1.5 Flash).
    Handles shared Gemini logic: authentication and prompt submission.
    """

    def _run_model_inference(self, records: list[dict]) -> str:
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)

        prompt = self.build_full_prompt(records)
        response = model.generate_content(prompt)

        return (response.text or "").strip()

