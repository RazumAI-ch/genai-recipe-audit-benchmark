# File: unit_tests/factory_unit_tests.py

import os
import importlib.util
import inspect
from typing import Type, Dict, List

import config.keys_unit_tests
from unit_tests.interface_unit_test import UnitTestInterface

ENABLED_UNIT_TESTS = config.keys_unit_tests.ENABLED_UNIT_TESTS
UNIT_TEST_REGISTRY: Dict[str, Type[UnitTestInterface]] = {}


def _load_unit_test_implementations():
    """
    Loads all unit test implementations from benchmark_unit_tests and training_unit_tests folders.
    Registers classes that:
    - Subclass UnitTestInterface
    - Are not abstract
    - Define a static/class field KEY
    """
    current_dir = os.path.dirname(__file__)
    subfolders = ["benchmark_unit_tests", "training_unit_tests"]

    for subfolder in subfolders:
        full_path = os.path.join(current_dir, subfolder)
        if not os.path.isdir(full_path):
            continue

        for filename in os.listdir(full_path):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue

            module_name = filename[:-3]
            module_path = os.path.join(full_path, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if not spec or not spec.loader:
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for _, cls in inspect.getmembers(module, inspect.isclass):
                if cls is UnitTestInterface:
                    continue
                if not issubclass(cls, UnitTestInterface):
                    continue
                if inspect.isabstract(cls):
                    continue
                if not hasattr(cls, "KEY"):
                    raise ValueError(f"Class {cls.__name__} in {filename} is missing required static field 'KEY'")

                UNIT_TEST_REGISTRY[cls.KEY] = cls


# Populate the registry
_load_unit_test_implementations()


class FactoryUnitTests:
    """
    Factory for dynamically loading and enabling unit tests for benchmark and training systems.
    """

    def __init__(self):
        self.unit_test_registry: Dict[str, Type[UnitTestInterface]] = UNIT_TEST_REGISTRY
        self.enabled_unit_tests = ENABLED_UNIT_TESTS

    def get_enabled_tests(self) -> List[UnitTestInterface]:
        """
        Returns a list of instantiated unit tests from the registry, limited to those marked as enabled.
        """
        return [cls() for key, cls in self.unit_test_registry.items() if key in self.enabled_unit_tests]