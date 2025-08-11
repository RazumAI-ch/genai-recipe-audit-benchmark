from __future__ import annotations

from typing import Dict, Any, Type

from benchmark_llms.providers.abstract_provider import AbstractProvider
from benchmark_llms.providers.utils.providers_autodiscovery import discover_providers


class FactoryProviders:
    """
    Provider factory.
    - Auto-discovers provider classes (no manual registry).
    - Instantiates the concrete provider for the model's provider key.
    """

    def __init__(self):
        # discovery returns: { "OPENAI": <OpenAIProvider>, "GEMINI_STUDIO": <...>, ... }
        self._registry: Dict[str, Type[AbstractProvider]] = discover_providers()

    def get_registry(self) -> Dict[str, Type[AbstractProvider]]:
        return dict(self._registry)

    def build(
        self,
        *,
        provider_name: str,           # e.g. "OPENAI"
        model_name: str,              # e.g. "gpt-4o"
        model_config: Dict[str, Any], # merged config for this model
    ) -> AbstractProvider:
        cls = self._registry.get(provider_name)
        if not cls:
            raise ValueError(
                f"No provider implementation registered for '{provider_name}'. "
                f"Known providers: {sorted(self._registry.keys())}"
            )

        # Do NOT pass provider_key here. Final class must provide it to super().__init__.
        instance = cls(
            model_name=model_name,
            model_config=model_config,
        )
        return instance