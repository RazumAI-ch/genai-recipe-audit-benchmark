# File: benchmark_llms/providers/utils/providers_autodiscovery.py

from __future__ import annotations
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, Type

import config.paths as config_paths
from benchmark_llms.providers.abstract_provider import AbstractProvider
from config.keys.keys_providers import LLMProviders


def _iter_provider_modules(base_dir: Path):
    """Yield (package_name, module_path) for provider implementation files."""
    if not base_dir.is_dir():
        print(f"[providers-autodiscovery] Base dir missing: {base_dir}")
        return

    children = list(base_dir.iterdir())
    print(f"[providers-autodiscovery] Directories under {base_dir}: {[p.name for p in children]}")

    for pkg_dir in children:
        if not pkg_dir.is_dir():
            print(f"[providers-autodiscovery] Skip non-dir: {pkg_dir.name}")
            continue

        # prefer provider.py; fall back to any *_provider.py
        cand = pkg_dir / "provider.py"
        if cand.is_file():
            print(f"[providers-autodiscovery] Found provider.py in {pkg_dir.name}: {cand}")
            yield pkg_dir.name, cand
            continue

        alts = list(pkg_dir.glob("*_provider.py"))
        if alts:
            for alt in alts:
                print(f"[providers-autodiscovery] Found alt provider in {pkg_dir.name}: {alt.name}")
                yield pkg_dir.name, alt
        else:
            print(f"[providers-autodiscovery] No provider module in {pkg_dir.name}")


def _load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if not spec or not spec.loader:
        raise ImportError(f"Could not load module spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
    except Exception as e:
        print(f"[providers-autodiscovery] IMPORT ERROR in {file_path}: {e}")
        raise
    return module


def discover_providers() -> Dict[str, Type[AbstractProvider]]:
    base_dir = Path(config_paths.PATH_PROVIDERS_IMPLEMENTATIONS_CODE)
    print(f"[providers-autodiscovery] Scanning: {base_dir.resolve()}")

    registry: Dict[str, Type[AbstractProvider]] = {}

    for pkg_name, module_path in _iter_provider_modules(base_dir):
        module_name = f"benchmark_llms.providers.implementations.{pkg_name}.{module_path.stem}"
        try:
            module = _load_module_from_path(module_name, module_path)
        except Exception:
            # keep scanning others, but we already logged the error above
            continue

        found_any = False
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if not issubclass(cls, AbstractProvider):
                continue
            if inspect.isabstract(cls):
                continue

            provider_key = getattr(cls, "provider_key", None)
            print(f"[providers-autodiscovery] Candidate class {cls.__name__} in {pkg_name} "
                  f"(provider_key={provider_key})")

            if not provider_key:
                continue

            if provider_key not in LLMProviders.all():
                raise ValueError(
                    f"{cls.__name__} has provider_key='{provider_key}', "
                    f"which is not in LLMProviders: {sorted(LLMProviders.all())}"
                )

            if provider_key in registry:
                other = registry[provider_key].__name__
                raise ValueError(
                    f"Duplicate provider_key '{provider_key}': {cls.__name__} conflicts with {other}"
                )

            registry[provider_key] = cls
            found_any = True
            print(f"[providers-autodiscovery] Registered: {provider_key} -> {cls.__name__}")

        if not found_any:
            print(f"[providers-autodiscovery] No concrete AbstractProvider subclasses found in {pkg_name}")

    if not registry:
        print("[providers-autodiscovery] No providers discovered.")
    return registry