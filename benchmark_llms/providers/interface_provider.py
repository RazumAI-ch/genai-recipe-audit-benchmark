# File: benchmark_llms/providers/interface_provider.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class InterfaceProvider(ABC):
    """
    Minimal, stable contract for all providers.

    A provider takes a *merged* model_config (from models.yaml + defaults + provider yaml),
    and exposes a single high-level `infer(...)` that returns the *raw* provider response
    (string) which higher layers will parse/normalize.
    """

    def __init__(self, model_config: Dict[str, Any]):
        self.model_config: Dict[str, Any] = model_config

    @property
    @abstractmethod
    def provider_key(self) -> str:
        """Return the canonical provider key (e.g., 'OPENAI', 'GEMINI_STUDIO')."""
        ...

    @abstractmethod
    def prepare(self) -> None:
        """
        Perform any one-time setup (read API key, init clients, validate config).
        Should raise if required config/env is missing.
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
        Execute inference for the batch of records and return the RAW textual response
        from the provider (the evaluated-LLM layer will parse/validate JSON).
        """
        ...