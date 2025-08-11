# File: benchmark_llms/utils/factory_evaluated_llms_from_models_yaml.py

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional

import yaml

import config.paths as config_paths
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager
from benchmark_llms.evaluated_llms.evaluated_llm_from_models_yaml import (
    EvaluatedLLMFromModelsYAML,
)


class FactoryEvaluatedLLMsFromModelsYAML:
    """
    MC1 factory that loads evaluated LLM configurations from config/models.yaml,
    merges defaults (global -> provider -> model), and instantiates concrete
    EvaluatedLLMFromModelsYAML objects that use the legacy base flow unchanged.
    """

    def __init__(self):
        self.logger = BenchmarkLogFileManager("_benchmark_factory_yaml")
        self.enabled_models: Dict[str, Dict[str, Any]] = self._load_models_from_yaml()

        self.logger.write_log(
            "startup",
            {"enabled_models": list(self.enabled_models.keys())},
        )

    # ---------------------------
    # Loading & merging config
    # ---------------------------
    def _load_models_from_yaml(self) -> Dict[str, Dict[str, Any]]:
        """
        Loads and resolves model configurations from models.yaml.
        Merge order:
            global_model_defaults
            provider_defaults[provider]
            models[model_key]
        Filters only enabled models.
        """
        config_path = Path(config_paths.PATH_CONFIG_MODELS_YAML)
        if not config_path.is_file():
            raise FileNotFoundError(f"models.yaml not found at {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        global_defaults = data.get("global_model_defaults", {}) or {}
        provider_defaults = data.get("provider_defaults", {}) or {}
        models = data.get("models", {}) or {}

        resolved_models: Dict[str, Dict[str, Any]] = {}
        for model_key, model_cfg in models.items():
            if not (model_cfg or {}).get("enabled", True):
                continue

            provider = (model_cfg or {}).get("provider")
            if not provider:
                raise ValueError(f"Model '{model_key}' is missing required field 'provider'.")

            merged_cfg: Dict[str, Any] = {}
            merged_cfg.update(global_defaults)
            merged_cfg.update(provider_defaults.get(provider, {}) or {})
            merged_cfg.update(model_cfg or {})

            # Inject api_key_env in the same place the legacy provider-layer merge would
            if "api_key_env" not in merged_cfg:
                merged_cfg["api_key_env"] = f"{provider}_API_KEY"
                print(f"DEBUG: {model_key} api_key_env -> {merged_cfg['api_key_env']}")

            # Ensure explicit enabled flag in the final dict
            merged_cfg["enabled"] = merged_cfg.get("enabled", True)

            resolved_models[model_key] = merged_cfg

        return resolved_models

    # ---------------------------
    # Public API
    # ---------------------------
    def get_enabled_models(self) -> Dict[str, Dict[str, Any]]:
        """Return enabled models and their merged configs."""
        return self.enabled_models

    def load_model(
        self,
        model_key: str,
        overrides: Optional[Dict[str, Any]] = None,
    ) -> EvaluatedLLMFromModelsYAML:
        """
        Instantiate the MC1 model wrapper for the given model_key using the merged config
        from models.yaml. Calls prepare() so it fully mirrors the legacy flow (sans inference).
        """
        cfg = self.enabled_models.get(model_key)
        if not cfg:
            raise ValueError(f"Model '{model_key}' is not enabled or not found in models.yaml.")

        model = EvaluatedLLMFromModelsYAML(model_key=model_key, model_config=cfg)
        model.prepare(overrides=overrides)
        return model