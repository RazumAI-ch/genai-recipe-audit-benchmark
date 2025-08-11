# File: benchmark_llms/providers/interface_provider.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class InterfaceProvider(ABC):
    """
    Minimal, stable contract for all providers.

    This defines HOW higher layers talk to providers, without
    constraining internal implementation details.

    All implementing classes must:
      - Provide their provider key via get_provider_key()
      - Execute inference via infer()
    """

    @abstractmethod
    def get_provider_key(self) -> str:
        """
        Return the canonical provider key (e.g., 'OPENAI', 'GEMINI_STUDIO').
        """
        ...

    @abstractmethod
    def infer(
        self,
        records: List[Dict[str, Any]],
        system_prompt: str,
        user_prompt_template: str,
        *,
        model: str,
        temperature: Optional[float],
        max_tokens: Optional[int],
        batch_size: Optional[int],
    ) -> str:
        """
        Execute inference for the given batch of records and return the
        RAW textual provider response.

        :param records: List of structured recipe records to audit.
        :param system_prompt: The system-level instruction text.
        :param user_prompt_template: The user prompt template text.
        :param model: Canonical model name from models.yaml.
        :param temperature: Optional temperature override.
        :param max_tokens: Optional max_tokens override.
        :param batch_size: Optional batch size override.
        :return: Raw provider output as a string.
        """
        ...