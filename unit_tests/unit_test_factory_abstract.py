# File: unit_tests/factory/unit_test_factory_abstract.py

import typing
import importlib
from unit_tests.unit_test_abstract import UnitTestInterface

class UnitTestFactoryAbstract:
    """
    Abstract factory class to manage registration and access of unit tests.
    Intended to be subclassed separately for benchmark and llm_training unit tests.

    Each subclass should define:
    - ENABLED_UNIT_TESTS: Set of test names to run
    - UNIT_TEST_REGISTRY: Dict of test names mapped to classes
    """

    ENABLED_UNIT_TESTS: typing.ClassVar[typing.Set[str]] = set()
    UNIT_TEST_REGISTRY: typing.ClassVar[typing.Dict[str, typing.Type[UnitTestInterface]]] = {}

    @classmethod
    def get_enabled_tests(cls) -> typing.List[UnitTestInterface]:
        """
        Return initialized instances of enabled tests.
        Ensures each one implements UnitTestInterface.
        """
        tests = []
        for test_name in cls.ENABLED_UNIT_TESTS:
            test_cls = cls.UNIT_TEST_REGISTRY.get(test_name)
            if not test_cls:
                raise ValueError(f"Unit test '{test_name}' not found in UNIT_TEST_REGISTRY.")

            instance = test_cls()
            if not isinstance(instance, UnitTestInterface):
                raise TypeError(f"Test '{test_name}' does not implement UnitTestInterface.")
            tests.append(instance)
        return tests

    @classmethod
    def list_available_tests(cls) -> typing.List[str]:
        return list(cls.UNIT_TEST_REGISTRY.keys())

    @classmethod
    def list_enabled_tests(cls) -> typing.List[str]:
        return list(cls.ENABLED_UNIT_TESTS)

    @classmethod
    def print_registry_summary(cls) -> None:
        print("\nRegistered Unit Tests:")
        for key in cls.UNIT_TEST_REGISTRY:
            enabled = "(enabled)" if key in cls.ENABLED_UNIT_TESTS else ""
            print(f"- {key} {enabled}")