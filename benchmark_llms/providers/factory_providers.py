# File: benchmark_llms/providers/factory_providers.py

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
        self._registry: Dict[str, Type[AbstractProvider]] = discover_providers()

    # --- New: convenience constructor to match call sites ---
    @classmethod
    def from_configs(cls) -> "FactoryProviders":
        """
        In future this can read config/providers/providers.yaml (defaults),
        but for now discovery alone is enough.
        """
        return cls()

    def get_registry(self) -> Dict[str, Type[AbstractProvider]]:
        return dict(self._registry)

    # --- New: 'build' to match call sites; keep old 'make_provider' as alias ---
    def build(
        self,
        *,
        provider_name: str,
        model_name: str,
        model_config: Dict[str, Any],
    ) -> AbstractProvider:
        cls = self._registry.get(provider_name)
        if not cls:
            raise ValueError(
                f"No provider implementation registered for '{provider_name}'. "
                f"Known: {sorted(self._registry.keys())}"
            )
        if not issubclass(cls, AbstractProvider):
            raise TypeError(
                f"Registered class for '{provider_name}' is not an AbstractProvider: {cls}"
            )
        return cls(provider_name=provider_name, model_name=model_name, model_config=model_config)

    # Back-compat alias (older call sites)
    make_provider = build