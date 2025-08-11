# File: benchmark_llms/utils/factory_providers.py

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import yaml
import config.paths as config_paths


class FactoryProviders:
    """
    Loads and resolves provider configurations from config/providers/*.yaml.
    Merge order:
      1. provider_defaults.all from models.yaml
      2. provider_defaults[PROVIDER] from models.yaml
      3. config/providers/{PROVIDER}.yaml
    """

    def __init__(self, provider_defaults_all: Dict[str, Any] = None, provider_defaults_specific: Dict[str, Any] = None):
        """
        :param provider_defaults_all: Defaults for all providers (from models.yaml -> provider_defaults.all)
        :param provider_defaults_specific: Dict of provider-specific defaults from models.yaml -> provider_defaults
        """
        self.provider_defaults_all = provider_defaults_all or {}
        self.provider_defaults_specific = provider_defaults_specific or {}

    def load_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Load provider configuration YAML for the given provider name.
        :param provider_name: The CAPSLOCK provider key from models.yaml
        :return: Merged configuration dictionary
        """
        # Path to provider YAML file
        provider_yaml_path = Path(config_paths.PATH_CONFIG_BASE) / "providers" / f"{provider_name}.yaml"
        if not provider_yaml_path.is_file():
            raise FileNotFoundError(f"Provider config not found: {provider_yaml_path}")

        with open(provider_yaml_path, "r", encoding="utf-8") as f:
            provider_yaml_data = yaml.safe_load(f) or {}

        # Merge: all → provider-specific defaults (from models.yaml) → provider YAML
        merged_cfg = {}
        merged_cfg.update(self.provider_defaults_all)
        merged_cfg.update(self.provider_defaults_specific.get(provider_name, {}) or {})
        merged_cfg.update(provider_yaml_data)

        return merged_cfg