# File: benchmark_llms/providers/abstract_provider.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json
import os

import yaml

import config.paths as config_paths
from config.keys.keys_llms import YAMLKeys
from config.keys.keys_providers import ProviderYAMLKeys as PK, LLMProviders
from benchmark_llms.providers.interface_provider import InterfaceProvider


class AbstractProvider(InterfaceProvider, ABC):
    """
    Base class for all provider implementations.

    Responsibilities handled here (so subclasses stay tiny):
      - Fail-fast contract: provider_key is required in __init__ (constant from LLMProviders).
      - Load & deep-merge provider config:
          providers.yaml (defaults) + providers/implementations/{PROVIDER}.yaml
      - Validate required runtime settings (base_url, http.*, api_key_env).
      - Resolve provider-specific endpoint model id via model_overrides.
      - Implement the high-level `infer(...)` orchestration:
          * format the user prompt (template + JSON batch)
          * call subclass `send_inference(...)`
      - Provide small helpers (auth header, deep-merge).

    Subclasses MUST implement:
      - send_inference(system_prompt, user_prompt, max_tokens, temperature) -> str
        (Single request returning the raw provider response text.)
    """

    def __init__(
        self,
        *,
        provider_key: str,              # Must be one of LLMProviders.*
        model_name: str,                # canonical model name from models.yaml
        model_config: Dict[str, Any],   # merged model config from the factory
    ):
        # ---------- Fail-fast: provider_key required & valid ----------
        if not provider_key:
            raise ValueError(f"{self.__class__.__name__} missing required `provider_key` in super().__init__.")
        if provider_key not in LLMProviders.all():
            raise ValueError(
                f"{self.__class__.__name__} got invalid provider_key='{provider_key}'. "
                f"Expected one of: {sorted(LLMProviders.all())}"
            )

        self.provider_key: str = provider_key
        self.model_name: str = model_name
        self.model_config: Dict[str, Any] = dict(model_config)

        # ---------- Load provider config (defaults + implementation) ----------
        self.provider_config: Dict[str, Any] = self._load_and_merge_provider_config(provider_key)

        # ---------- Validate required runtime config ----------
        # base_url
        self.base_url: Optional[str] = self.provider_config.get(PK.BASE_URL)
        self._require(self.base_url, f"Missing '{PK.BASE_URL}' in provider config for {provider_key}.")

        # http settings (allow per-model override; else provider config)
        http_cfg: Optional[Dict[str, Any]] = self.model_config.get(PK.HTTP) or self.provider_config.get(PK.HTTP)
        self._require(http_cfg, f"Missing '{PK.HTTP}' section in model or provider config for {provider_key}.")
        for k in (PK.HTTP_TIMEOUT, PK.HTTP_MAX_RETRIES, PK.HTTP_RATE_SLEEP):
            self._require(k in http_cfg, f"Missing '{k}' in '{PK.HTTP}' for provider {provider_key}.")

        self.timeout_seconds: int = http_cfg[PK.HTTP_TIMEOUT]
        self.max_retries: int = http_cfg[PK_HTTP_MAX_RETRIES] if (PK_HTTP_MAX_RETRIES := PK.HTTP_MAX_RETRIES) else http_cfg[PK.HTTP_MAX_RETRIES]  # type: ignore[name-defined]
        self.rate_limit_sleep: float = http_cfg[PK.HTTP_RATE_SLEEP]

        # endpoint model id mapping
        self.endpoint_model_id: str = self._map_endpoint_model_id(
            model_name=self.model_name,
            provider_cfg=self.provider_config,
        )

        # api key
        api_key_env_name: Optional[str] = self.model_config.get("api_key_env") or self.provider_config.get("api_key_env")
        self._require(api_key_env_name, "Missing 'api_key_env' in model or provider config.")
        self.api_key_env: str = api_key_env_name  # type: ignore[assignment]
        self.api_key: Optional[str] = os.getenv(self.api_key_env)
        self._require(self.api_key, f"Environment variable '{self.api_key_env}' is not set.")

    # ---------------------------------------------------------------------
    # Public high-level entrypoint (common to all providers)
    # ---------------------------------------------------------------------
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
        Common inference orchestration:
          - Renders a single user prompt for the batch (template + pretty JSON of records)
          - Calls subclass `send_inference(...)`
          - Returns raw response text
        """
        # Build the concrete user prompt sent to the provider
        # (Keep this consistent with AbstractEvaluatedLLMBase.build_full_prompt)
        user_prompt = (
            f"{user_prompt_template}\n\n"
            "Recipe data:\n"
            f"{json.dumps(records, indent=2, sort_keys=True)}"
        )

        # Allow model_config values to be overridden by explicit args if present
        eff_temperature = temperature if temperature is not None else self.model_config.get(YAMLKeys.TEMPERATURE)
        eff_max_tokens = max_tokens if max_tokens is not None else self.model_config.get(YAMLKeys.MAX_TOKENS)

        # Delegate the actual network call to subclass
        raw = self.send_inference(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=eff_max_tokens,
            temperature=eff_temperature,
        )
        return raw

    # ---------------------------------------------------------------------
    # Interface contract convenience (so subclasses don't have to)
    # ---------------------------------------------------------------------
    def get_provider_key(self) -> str:
        """Return the canonical provider key for this provider."""
        return self.provider_key

    # ---------------------------------------------------------------------
    # Subclass hook: must implement the concrete request/parse
    # ---------------------------------------------------------------------
    @abstractmethod
    def send_inference(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: Optional[int],
        temperature: Optional[float],
    ) -> str:
        """Execute a single provider request and return the raw textual response."""
        raise NotImplementedError

    # ---------------------------------------------------------------------
    # Config loading & helpers
    # ---------------------------------------------------------------------
    def _load_and_merge_provider_config(self, provider_key: str) -> Dict[str, Any]:
        """
        Merge order (lowest → highest precedence):
          1) providers.yaml: provider_defaults        (defaults for ALL providers)
          2) providers/implementations/{PROVIDER}.yaml
        Accepts dotted http.* in defaults and normalizes to a nested 'http' block.
        """
        # 1) providers.yaml (flat defaults)
        try:
            with open(config_paths.PATH_CONFIG_PROVIDERS_YAML, "r", encoding="utf-8") as f:
                providers_root = yaml.safe_load(f) or {}
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"providers.yaml not found at {config_paths.PATH_CONFIG_PROVIDERS_YAML}"
            ) from e

        defaults = providers_root.get("provider_defaults") or {}

        # 2) implementations/{PROVIDER}.yaml (runtime cfg)
        impl_path = f"{config_paths.PATH_CONFIG_PROVIDERS_IMPLEMENTATIONS}/{provider_key}.yaml"
        try:
            with open(impl_path, "r", encoding="utf-8") as f:
                impl_cfg = yaml.safe_load(f) or {}
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Provider implementation config not found: {impl_path}") from e

        # Deep-merge: defaults -> impl
        merged: Dict[str, Any] = {}
        merged = self._deep_merge(merged, defaults)
        merged = self._deep_merge(merged, impl_cfg)

        # Normalize HTTP: allow dotted keys in defaults
        merged = self._normalize_http_block(merged)

        return merged

    @staticmethod
    def _normalize_http_block(cfg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accept dotted http.* keys and synthesize a nested 'http' block if missing.
        """
        if "http" not in cfg:
            dotted = {
                k.split(".", 1)[1]: v
                for k, v in cfg.items()
                if isinstance(k, str) and k.startswith("http.") and "." in k
            }
            if dotted:
                cfg = dict(cfg)
                cfg["http"] = dotted
        return cfg

    @staticmethod
    def _deep_merge(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in (src or {}).items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                dst[k] = AbstractProvider._deep_merge(dst[k], v)
            else:
                dst[k] = v
        return dst

    @staticmethod
    def _require(condition: Any, message: str) -> None:
        if not condition:
            raise ValueError(message)

    def _map_endpoint_model_id(self, *, model_name: str, provider_cfg: Dict[str, Any]) -> str:
        """Map canonical model -> provider endpoint model id via model_overrides (optional)."""
        overrides = provider_cfg.get(PK.MODEL_OVERRIDES) or {}
        if not isinstance(overrides, dict):
            raise ValueError(f"'{PK.MODEL_OVERRIDES}' must be a mapping if present.")
        entry = overrides.get(model_name) or {}
        if entry and not isinstance(entry, dict):
            raise ValueError(f"'{PK.MODEL_OVERRIDES}[{model_name}]' must be a mapping if present.")
        return entry.get(PK.ENDPOINT_MODEL_ID) or model_name

    # Default auth header helper (Bearer)
    def build_auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}