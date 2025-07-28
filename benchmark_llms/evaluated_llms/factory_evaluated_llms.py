# File: benchmark_llms/evaluated_llms/factory_evaluated_llms.py

import os
import importlib.util
import inspect
import typing
from typing import Type, Dict, Any

import config.keys_evaluated_llms as config_keys_evaluated_llms
from benchmark_llms.evaluated_llms.interface_evaluated_llm import InterfaceEvaluatedLLM  # ✅ corrected class name

# Define which models are currently enabled for evaluation (manually managed)
ENABLED_MODELS = config_keys_evaluated_llms.ENABLED_BENCHMARK_MODELS

# Dynamically populated: ModelKey → Implementation Class
MODEL_REGISTRY: Dict[str, Type[InterfaceEvaluatedLLM]] = {}


def _load_model_implementations():
    """
    Dynamically loads all classes from 'implementations' that:
    - Subclass InterfaceEvaluatedLLM (but are not the interface itself)
    - Are not abstract (we assume concrete implementations only)
    Registers via get_model_key()
    """
    impl_dir = os.path.join(os.path.dirname(__file__), "implementations")

    for filename in os.listdir(impl_dir):
        if not filename.endswith(".py") or filename.startswith("_"):
            continue

        module_name = filename[:-3]
        module_path = os.path.join(impl_dir, filename)

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if not spec or not spec.loader:
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if cls is InterfaceEvaluatedLLM:
                continue
            if not issubclass(cls, InterfaceEvaluatedLLM):
                continue
            if inspect.isabstract(cls):
                continue

            try:
                model_key = cls.get_model_key()  # ✅ enforce interface usage
            except Exception as e:
                raise TypeError(f"Class {cls.__name__} failed get_model_key(): {e}")

            MODEL_REGISTRY[model_key] = cls


# Populate the model registry at import time
_load_model_implementations()


class FactoryEvaluatedLLMs:
    """
    Factory class responsible for registering and running all enabled benchmark_llms LLMs.
    """

    def __init__(self):
        self.model_registry: Dict[str, Type[InterfaceEvaluatedLLM]] = MODEL_REGISTRY
        self.enabled_models: typing.Set[str] = ENABLED_MODELS

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