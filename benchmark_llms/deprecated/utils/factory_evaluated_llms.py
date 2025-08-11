# File: benchmark_llms/evaluated_llms/factory_evaluated_llms.py
# One-time legacy factory (MC0) used only to keep parity while MC1 (models.yaml + providers)
# comes online. Safe to remove after MC1.1 when legacy impls are fully retired.

import importlib.util
import inspect
import typing
from typing import Type, Dict, Any
from pathlib import Path
import sys

import config.keys.keys_llms as config_keys_evaluated_llms
from benchmark_llms.evaluated_llms.interface_evaluated_llm import InterfaceEvaluatedLLM
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager

# Models to exclude from execution (everything else is enabled)
DISABLED_MODELS = config_keys_evaluated_llms.DISABLED_BENCHMARK_MODELS

# Dynamically populated: ModelKey → Implementation Class
MODEL_REGISTRY: Dict[str, Type[InterfaceEvaluatedLLM]] = {}


def _load_model_implementations() -> None:
    """
    Scan the legacy implementations folder and register final classes.

    A class is considered "final" if:
      - It subclasses InterfaceEvaluatedLLM
      - It defines 'ModelKey' directly on the class (not inherited)
    """
    import config.paths as config_paths
    impl_dir = Path(config_paths.PATH_BENCHMARK_EVALUATED_LLM_IMPLEMENTATIONS)

    # Loud debug so it’s obvious WHERE we’re scanning
    try:
        print(f"[LEGACY-FACTORY] Scanning for implementations in: {impl_dir.resolve()}")
    except Exception:
        print(f"[LEGACY-FACTORY] Scanning for implementations in: {impl_dir}")

    if not impl_dir.is_dir():
        # Don’t raise — allow MC1 path to run even if legacy folder was moved/removed.
        print(
            f"[LEGACY-FACTORY] WARNING: Implementation directory not found: "
            f"{config_paths.PATH_BENCHMARK_EVALUATED_LLM_IMPLEMENTATIONS}. Skipping legacy scan."
        )
        return

    # Deterministic order for reproducible logs
    for py_file in sorted(impl_dir.rglob("*.py"), key=lambda p: str(p).lower()):
        # ignore private files, pycache, and anything that isn't a file
        if py_file.name.startswith("_"):
            continue
        if "__pycache__" in py_file.parts or not py_file.is_file():
            continue

        module_name = f"legacy_impl__{py_file.stem}"  # ensure uniqueness across files
        module_path = str(py_file.resolve())

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if not spec or not spec.loader:
            print(f"[LEGACY-FACTORY] SKIP (no loader): {module_path}")
            continue

        try:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore[attr-defined]
        except Exception as e:
            # Keep going even if one implementation fails to import
            print(f"[LEGACY-FACTORY] IMPORT FAIL in {module_path}: {e}", file=sys.stderr)
            continue

        finals = []
        for _, cls in inspect.getmembers(module, inspect.isclass):
            # hard-skip the interface itself
            if cls is InterfaceEvaluatedLLM:
                continue
            if not issubclass(cls, InterfaceEvaluatedLLM):
                continue
            # Must define 'ModelKey' directly on the class (not inherited)
            if InterfaceEvaluatedLLM.REQUIRED_STATIC_FIELD not in cls.__dict__:
                continue
            finals.append(cls)

        if len(finals) > 1:
            print(
                f"[LEGACY-FACTORY] WARN: Multiple final classes in {module_path}: "
                f"{[c.__name__ for c in finals]}"
            )

        for cls in finals:
            try:
                model_key = cls.get_model_key()
            except Exception as e:
                print(f"[LEGACY-FACTORY] WARN: Could not get ModelKey from {cls}: {e}", file=sys.stderr)
                continue

            if model_key in MODEL_REGISTRY:
                print(f"[LEGACY-FACTORY] ERROR: Duplicate ModelKey detected: {model_key}", file=sys.stderr)
                continue

            MODEL_REGISTRY[model_key] = cls
            print(f"[LEGACY-FACTORY] Registered legacy model: {model_key} -> {cls.__module__}.{cls.__name__}")


# Populate the model registry at import time (safe if folder is missing)
_load_model_implementations()


class FactoryEvaluatedLLMs:
    """
    Legacy factory responsible for registering and running all enabled evaluated LLMs.
    Kept only to validate parity during MC1 bring‑up. Remove after MC1.1.
    """

    def __init__(self):
        self.model_registry: Dict[str, Type[InterfaceEvaluatedLLM]] = MODEL_REGISTRY
        self.disabled_models: typing.Set[str] = DISABLED_MODELS
        self.enabled_models: typing.Set[str] = {
            k for k in self.model_registry.keys() if k not in self.disabled_models
        }

        self.logger = BenchmarkLogFileManager("_benchmark_factory")
        self.logger.write_log(
            "startup",
            {
                "registered_models": list(self.model_registry.keys()),
                "enabled_models": list(self.enabled_models),
                "disabled_models": list(self.disabled_models),
            },
        )

    def get_enabled_models(self) -> Dict[str, Type[InterfaceEvaluatedLLM]]:
        """Return only enabled models."""
        return {k: v for k, v in self.model_registry.items() if k in self.enabled_models}

    def load_model(
        self,
        model_name: str,
        overrides: typing.Optional[Dict[str, Any]] = None,
    ) -> InterfaceEvaluatedLLM:
        """
        Instantiate a model class from the registry using the given name.
        Applies optional overrides (e.g., to change model version or batch size).
        """
        model_class = self.model_registry.get(model_name)
        if not model_class:
            raise ValueError(f"Model '{model_name}' is not registered.")
        model: InterfaceEvaluatedLLM = model_class()
        model.prepare(overrides=overrides)
        return model