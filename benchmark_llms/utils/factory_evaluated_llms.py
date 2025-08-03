# File: benchmark_llms/evaluated_llms/factory_evaluated_llms.py

import os
import importlib.util
import inspect
import typing
from typing import Type, Dict, Any
from pathlib import Path

import config.keys_evaluated_llms as config_keys_evaluated_llms
from benchmark_llms.evaluated_llms.interface_evaluated_llm import InterfaceEvaluatedLLM
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager

# Models to exclude from execution (everything else is enabled)
DISABLED_MODELS = config_keys_evaluated_llms.DISABLED_BENCHMARK_MODELS

# Dynamically populated: ModelKey → Implementation Class
MODEL_REGISTRY: Dict[str, Type[InterfaceEvaluatedLLM]] = {}


def _load_model_implementations():
    """
    Loads all final evaluated LLM implementations from the implementations folder.
    A class is considered final if:
    - It subclasses InterfaceEvaluatedLLM
    - It defines 'ModelKey' directly (not inherited)
    """
    import config.paths as config_paths
    impl_dir = Path(config_paths.PATH_BENCHMARK_EVALUATED_LLM_IMPLEMENTATIONS)

    if not impl_dir.is_dir():
        raise FileNotFoundError(f"Model implementation directory not found: {impl_dir}")

    for py_file in impl_dir.rglob("*.py"):
        if py_file.name.startswith("_"):
            continue

        module_name = py_file.stem
        module_path = str(py_file.resolve())

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if not spec or not spec.loader:
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if not issubclass(cls, InterfaceEvaluatedLLM):
                continue
            if InterfaceEvaluatedLLM.REQUIRED_STATIC_FIELD not in cls.__dict__:
                continue

            model_key = cls.get_model_key()

            if model_key in MODEL_REGISTRY:
                raise ValueError(f"Duplicate ModelKey detected: {model_key}")

            MODEL_REGISTRY[model_key] = cls


# Populate the model registry at import time
_load_model_implementations()


class FactoryEvaluatedLLMs:
    """
    Factory class responsible for registering and running all enabled benchmark_llms LLMs.
    """

    def __init__(self):
        self.model_registry: Dict[str, Type[InterfaceEvaluatedLLM]] = MODEL_REGISTRY
        self.disabled_models: typing.Set[str] = DISABLED_MODELS
        self.enabled_models: typing.Set[str] = {
            k for k in self.model_registry.keys() if k not in self.disabled_models
        }

        self.logger = BenchmarkLogFileManager("_benchmark_factory")
        self.logger.write_log("startup", {
            "registered_models": list(self.model_registry.keys()),
            "enabled_models": list(self.enabled_models),
            "disabled_models": list(self.disabled_models)
        })

    def get_enabled_models(self) -> Dict[str, Type[InterfaceEvaluatedLLM]]:
        """
        Returns a filtered version of the model registry that includes only enabled models.
        """
        return {k: v for k, v in self.model_registry.items() if k in self.enabled_models}

    def load_model(self, model_name: str, overrides: typing.Optional[Dict[str, Any]] = None) -> InterfaceEvaluatedLLM:
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