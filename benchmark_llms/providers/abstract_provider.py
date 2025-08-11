# File: benchmark_llms/providers/abstract_provider.py

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import yaml

import config.paths as config_paths
from config.keys.keys_providers import ProviderYAMLKeys as PK, LLMProviders
from benchmark_llms.providers.interface_provider import InterfaceProvider


class AbstractProvider(InterfaceProvider, ABC):
    """
    Base class for provider implementations.

    Responsibilities:
    - Load & deep-merge provider-level config:
        providers.yaml (defaults) + implementations/{PROVIDER}.yaml (runtime cfg)
      * providers.yaml contains ONLY defaults (no provider-specific sections).
      * provider implementation YAML holds base_url, optional http.*, model_overrides.
    - Normalize dotted keys (e.g., "http.timeout_seconds") into nested dicts.
    - Resolve runtime params strictly from config (no code *value* defaults).
    - Map canonical `model` -> provider endpoint model id via `model_overrides`.
    - Resolve API key from env. If not specified in config, derive as {PROVIDER}_API_KEY
      (deterministic, not a magic default; aligns with repo policy).
    """

    # Concrete classes MUST set this to one of LLMProviders.* (e.g., "OPENAI")
    provider_key: str

    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        model_config: Dict[str, Any],
    ):
        """
        :param provider_name: Provider key from models.yaml (e.g., 'OPENAI').
        :param model_name: Canonical model string from models.yaml (e.g., 'gpt-4o').
        :param model_config: Already-merged models.yaml entry for this model (factory output).
        """
        # Validate concrete class declares provider_key and matches requested provider
        if not getattr(self, "provider_key", None):
            raise ValueError(f"{self.__class__.__name__} must set provider_key to a value in LLMProviders.")
        if self.provider_key not in LLMProviders.all():
            raise ValueError(f"Invalid provider_key '{self.provider_key}' in {self.__class__.__name__}.")
        if self.provider_key != provider_name:
            raise ValueError(
                f"{self.__class__.__name__} provider_key='{self.provider_key}' "
                f"does not match requested provider '{provider_name}'."
            )

        self.provider_name = provider_name
        self.model_name = model_name
        self.model_config: Dict[str, Any] = dict(model_config)

        # Load provider config (providers.yaml defaults + implementation YAML)
        self.provider_config: Dict[str, Any] = self._load_and_merge_provider_config(provider_name)

        # ---- Resolve base_url (required)
        self.base_url: Optional[str] = self.provider_config.get(PK.BASE_URL)
        self._require(self.base_url, f"Missing '{PK.BASE_URL}' in provider config for {provider_name}.")

        # ---- Resolve HTTP settings (required)
        # Prefer model_config.http override, then merged provider_config.http
        http_cfg: Optional[Dict[str, Any]] = (
            self.model_config.get(PK.HTTP) or
            self.provider_config.get(PK.HTTP)
        )
        self._require(http_cfg, f"Missing '{PK.HTTP}' section in model or provider config for {provider_name}.")

        for k in (PK.HTTP_TIMEOUT, PK.HTTP_MAX_RETRIES, PK.HTTP_RATE_SLEEP):
            self._require(k in http_cfg, f"Missing '{k}' in '{PK.HTTP}' for provider {provider_name}.")

        self.timeout_seconds: int = http_cfg[PK.HTTP_TIMEOUT]
        self.max_retries: int = http_cfg[PK.HTTP_MAX_RETRIES]
        self.rate_limit_sleep: float = http_cfg[PK.HTTP_RATE_SLEEP]

        # ---- Resolve endpoint model id mapping (optional; fallback to canonical)
        self.endpoint_model_id: str = self._map_endpoint_model_id(
            model_name=self.model_name,
            provider_cfg=self.provider_config,
        )

        # ---- Resolve API key from env
        # Order: model_config.api_key_env -> provider_config.api_key_env -> f"{PROVIDER}_API_KEY"
        api_key_env_name: Optional[str] = (
            self.model_config.get("api_key_env") or
            self.provider_config.get("api_key_env") or
            f"{provider_name}_API_KEY"
        )
        self._require(api_key_env_name, "Missing 'api_key_env' (could not derive from provider key).")

        self.api_key_env: str = api_key_env_name
        self.api_key: Optional[str] = os.getenv(self.api_key_env)
        self._require(self.api_key, f"Environment variable '{self.api_key_env}' is not set.")

    # ---------------------------------------------------------------------
    # Abstracts that concrete providers must implement
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
        """Execute a single inference call and return raw text."""
        raise NotImplementedError

    # ---------------------------------------------------------------------
    # Internal config loading/merging
    # ---------------------------------------------------------------------
    def _load_and_merge_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Load providers.yaml defaults + implementations/{PROVIDER}.yaml and deep-merge.

        providers.yaml shape (minimal):
          provider_defaults:
            http.timeout_seconds: 60
            http.max_retries: 3
            http.rate_limit_sleep: 2

        We normalize dotted keys (e.g., "http.timeout_seconds") into nested dicts:
          { "http": { "timeout_seconds": 60, ... } }
        """
        # 1) providers.yaml defaults
        defaults_root: Dict[str, Any] = {}
        try:
            with open(config_paths.PATH_CONFIG_PROVIDERS_YAML, "r", encoding="utf-8") as f:
                defaults_root = yaml.safe_load(f) or {}
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"providers.yaml not found at {config_paths.PATH_CONFIG_PROVIDERS_YAML}"
            ) from e

        prov_defaults = defaults_root.get("provider_defaults") or {}
        # Support both flattened (new) and legacy (_ALL_/per-provider) shapes gracefully
        if isinstance(prov_defaults, dict) and any("." in k for k in prov_defaults.keys()):
            # New shape: flat dotted keys right under provider_defaults
            defaults_all = self._undot_keys(prov_defaults)
            defaults_specific = {}
        else:
            # Legacy shape: _ALL_ and/or {PROVIDER} submaps
            defaults_all = self._undot_keys(prov_defaults.get("_ALL_", {}) or {})
            defaults_specific = self._undot_keys(prov_defaults.get(provider_name, {}) or {})

        # 2) implementations/{PROVIDER}.yaml
        impl_path = f"{config_paths.PATH_CONFIG_PROVIDERS_IMPLEMENTATIONS}/{provider_name}.yaml"
        try:
            with open(impl_path, "r", encoding="utf-8") as f:
                impl_cfg_raw = yaml.safe_load(f) or {}
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Provider implementation config not found: {impl_path}"
            ) from e
        impl_cfg = self._undot_keys(impl_cfg_raw)

        # 3) deep-merge: ALL -> specific -> impl
        merged = self._deep_merge({}, defaults_all)
        merged = self._deep_merge(merged, defaults_specific)
        merged = self._deep_merge(merged, impl_cfg)

        return merged

    def _map_endpoint_model_id(self, *, model_name: str, provider_cfg: Dict[str, Any]) -> str:
        overrides = provider_cfg.get(PK.MODEL_OVERRIDES) or {}
        if not isinstance(overrides, dict):
            raise ValueError(f"'{PK.MODEL_OVERRIDES}' must be a mapping if present.")
        entry = overrides.get(model_name) or {}
        if entry and not isinstance(entry, dict):
            raise ValueError(f"'{PK.MODEL_OVERRIDES}[{model_name}]' must be a mapping if present.")
        return entry.get(PK.ENDPOINT_MODEL_ID) or model_name

    @staticmethod
    def _undot_keys(flat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert dotted keys into nested dicts.
        Example:
          { "http.timeout_seconds": 60 } -> { "http": { "timeout_seconds": 60 } }
        """
        out: Dict[str, Any] = {}
        for k, v in (flat or {}).items():
            if "." not in k:
                # Recurse if nested mapping is present
                out[k] = AbstractProvider._undot_keys(v) if isinstance(v, dict) else v
                continue
            head, *rest = k.split(".")
            tail = ".".join(rest)
            node = out.setdefault(head, {})
            if not isinstance(node, dict):
                raise ValueError(f"Key collision while undotting '{k}'.")
            # Assign (recursively undot the tail)
            value_dict = AbstractProvider._undot_keys({tail: v}) if "." in tail else {tail: v}
            out[head] = AbstractProvider._deep_merge(node, value_dict)
        return out

    @staticmethod
    def _deep_merge(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in (src or {}).items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                dst[k] = AbstractProvider._deep_merge(dst[k], v)
            else:
                dst[k] = v
        return dst

    def _require(self, condition: Any, message: str) -> None:
        if not condition:
            raise ValueError(message)

    # Default auth header helper
    def build_auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}