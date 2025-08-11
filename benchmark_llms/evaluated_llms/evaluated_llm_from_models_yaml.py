# File: benchmark_llms/evaluated_llms/evaluated_llm_from_models_yaml.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

from benchmark_llms.evaluated_llms.abstract_evaluated_llm_base import (
    AbstractEvaluatedLLMBase,
)
from config.keys.keys_llms import YAMLKeys, MODEL
from benchmark_llms.providers.factory_providers import FactoryProviders
from benchmark_llms.evaluated_llms.utils.response_utils import parse_model_response


class EvaluatedLLMFromModelsYAML(AbstractEvaluatedLLMBase):
    """
    MC1 (models.yaml-driven) evaluated LLM.

    Differences from legacy:
      - Config comes from merged models.yaml (factory-injected) instead of per-model YAML.
      - Inference is delegated to a concrete Provider (via FactoryProviders).
    """

    def __init__(self, model_key: str, model_config: Dict[str, Any]):
        # Set static ModelKey exactly as legacy expects
        type(self).ModelKey = model_key

        # Stash merged config so _load_config() can return it
        self._injected_model_config: Dict[str, Any] = dict(model_config)

        # Normal base init (loads prompts, etc.), which calls _load_config()
        super().__init__()

        # Handy shortcuts (also finalized in prepare())
        self.model: str = self.model_config.get(MODEL)
        self.batch_size: Optional[int] = self.model_config.get(YAMLKeys.BATCH_SIZE)
        self.temperature: Optional[float] = self.model_config.get(YAMLKeys.TEMPERATURE)
        self.max_tokens: Optional[int] = self.model_config.get(YAMLKeys.MAX_TOKENS)

        self._provider = None  # set in prepare()

    # Return injected merged config instead of reading per-model YAML
    def _load_config(self, path: str) -> Dict[str, Any]:
        return self._injected_model_config

    @classmethod
    def get_model_key(cls) -> str:
        if not getattr(cls, "ModelKey", None):
            raise ValueError(f"{cls.__name__} must define a static 'ModelKey'.")
        return cls.ModelKey  # type: ignore[attr-defined]

    def prepare(self, overrides: Optional[Dict[str, Any]] = None) -> None:
        """
        Normal prepare flow (prompts, overrides, etc.), plus:
          - build a Provider instance based on provider+model from models.yaml.
        """
        super().prepare(overrides=overrides)

        factory = FactoryProviders.from_configs()
        self._provider = factory.build(
            provider_name=self.model_config[YAMLKeys.PROVIDER],
            model_name=self.model,
            model_config=self.model_config,
        )

    def _run_model_inference(self, records: List[Dict[str, Any]]) -> str:
        """
        Route inference to the configured Provider and return the raw response text.
        Also validate that the response parses into the expected JSON structure.
        """
        if self._provider is None:
            raise RuntimeError("Provider not initialized. Call prepare() first.")

        raw = self._provider.infer(
            records=records,
            system_prompt=self.system_prompt,      # from base.prepare()
            user_prompt_template=self.user_prompt, # from base.prepare()
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            batch_size=self.batch_size,
        )

        # Early validation (keeps downstream stable); raises on invalid JSON
        _ = parse_model_response(raw)
        return raw

    def __repr__(self) -> str:
        return f"<EvaluatedLLMFromModelsYAML key={self.ModelKey} model={self.model}>"