# File: benchmark_llms/providers/utils/providers_autodiscovery.py

from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Dict, Type, Optional

import config.paths as config_paths
from benchmark_llms.providers.abstract_provider import AbstractProvider
from config.keys.keys_providers import LLMProviders


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if not spec or not spec.loader:
        raise ImportError(f"Could not load module spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def _pick_single_py_in_dir(pkg_dir: Path) -> Optional[Path]:
    """
    Enforce exactly one top-level .py file per provider folder.
    - Ignores __init__.py and files starting with '_'
    - Does NOT scan subfolders (e.g., utils/ is allowed and ignored)
    """
    candidates = [
        p for p in pkg_dir.iterdir()
        if p.is_file() and p.suffix == ".py" and p.name != "__init__.py" and not p.name.startswith("_")
    ]
    if not candidates:
        print(f"[providers-autodiscovery] No .py file found in {pkg_dir.name}")
        return None
    if len(candidates) > 1:
        names = [c.name for c in candidates]
        raise ValueError(
            f"[providers-autodiscovery] Multiple .py files found in provider folder '{pkg_dir.name}': {names}. "
            f"Keep exactly one."
        )
    return candidates[0]


def _extract_provider_key(pkg_name: str, cls) -> Optional[str]:
    """
    Determine provider_key for the class:
    1) class attribute 'provider_key'
    2) class attribute 'PROVIDER_KEY'
    3) folder name uppercased (must exist in LLMProviders)
    """
    key = getattr(cls, "provider_key", None) or getattr(cls, "PROVIDER_KEY", None)
    if key:
        return key
    # Fallback: derive from folder name (OPENAI, GEMINI_STUDIO, etc.)
    derived = pkg_name.upper()
    if derived in LLMProviders.all():
        print(f"[providers-autodiscovery] provider_key not declared on {cls.__name__}; "
              f"using derived key from folder '{pkg_name}' -> '{derived}'")
        return derived
    return None


def discover_providers() -> Dict[str, Type[AbstractProvider]]:
    """
    Discover provider implementations using the 'one file per folder' rule.

    Folder layout:
      benchmark_llms/providers/implementations/
        OPENAI/      <- folder name may be 'openai' or 'OPENAI'
          provider.py <- the ONLY top-level .py file for this provider
          utils/      <- (optional) any support code here (ignored by discovery)

    Registration rule:
      - Load that single .py file
      - Find classes that either subclass AbstractProvider OR at least declare provider_key/PROVIDER_KEY
      - Resolve provider_key via class attr (preferred) or folder name (fallback)
      - Register mapping: provider_key -> class
    """
    base_dir = Path(config_paths.PATH_PROVIDERS_IMPLEMENTATIONS_CODE)

    try:
        print(f"[providers-autodiscovery] Scanning for providers in: {base_dir.resolve()}")
    except Exception:
        print(f"[providers-autodiscovery] Scanning for providers in: {base_dir}")

    registry: Dict[str, Type[AbstractProvider]] = {}

    if not base_dir.is_dir():
        print(f"[providers-autodiscovery] WARNING: Implementation directory not found: {base_dir}")
        return registry

    for pkg_dir in sorted(base_dir.iterdir(), key=lambda p: p.name.lower()):
        if not pkg_dir.is_dir():
            print(f"[providers-autodiscovery] Skip non-dir: {pkg_dir.name}")
            continue

        py_file = _pick_single_py_in_dir(pkg_dir)
        if not py_file:
            continue

        print(f"[providers-autodiscovery] Loading {py_file} for provider folder '{pkg_dir.name}'")
        module_name = f"provider_impl__{pkg_dir.name.lower()}"
        try:
            module = _load_module(module_name, py_file)
        except Exception as e:
            print(f"[providers-autodiscovery] IMPORT FAIL in {py_file}: {e}", file=sys.stderr)
            continue

        finals = []
        for _, cls in inspect.getmembers(module, inspect.isclass):
            # Prefer strict check, but allow classes that declare a provider_key even if
            # AbstractProvider import path mismatch would break issubclass()
            issub = False
            try:
                issub = issubclass(cls, AbstractProvider) and (cls is not AbstractProvider)
            except Exception:
                issub = False

            has_key_attr = hasattr(cls, "provider_key") or hasattr(cls, "PROVIDER_KEY")
            if issub or has_key_attr:
                finals.append(cls)

        if not finals:
            print(f"[providers-autodiscovery] No eligible provider class found in {pkg_dir.name}")
            continue

        if len(finals) > 1:
            print(f"[providers-autodiscovery] WARN: Multiple candidate classes in {py_file}: "
                  f"{[c.__name__ for c in finals]}. Taking the first by class name.")
            finals = sorted(finals, key=lambda c: c.__name__)

        cls = finals[0]
        provider_key = _extract_provider_key(pkg_dir.name, cls)

        if not provider_key:
            print(f"[providers-autodiscovery] SKIP {cls.__name__}: cannot resolve provider_key "
                  f"(folder='{pkg_dir.name}')")
            continue

        if provider_key in registry:
            other = registry[provider_key].__name__
            raise ValueError(
                f"[providers-autodiscovery] Duplicate provider_key '{provider_key}': "
                f"{cls.__name__} conflicts with {other}"
            )

        registry[provider_key] = cls
        print(f"[providers-autodiscovery] Registered provider: {provider_key} -> {cls.__module__}.{cls.__name__}")

    if not registry:
        print("[providers-autodiscovery] No providers discovered.")
    return registry