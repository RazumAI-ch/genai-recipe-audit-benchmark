# File: unit_tests/benchmark_tests/benchmark_test_factory.py

import unit_tests.unit_test_factory_abstract as unit_test_factory_interface
import unit_tests.unit_test_abstract as unit_test_abstract

# Example test: you will replace this with real ones
from unit_tests.benchmark_tests.core.test_schema_sync import SchemaDocsSyncTest


class BenchmarkTestFactory(unit_test_factory_interface.UnitTestFactoryInterface):
    """
    Concrete factory that registers all unit tests relevant to the benchmark pipeline.
    Provides a list of enabled test instances implementing UnitTestInterface.
    """

    def __init__(self):
        self.registry = []
        self._register_tests()

    def _register_tests(self):
        # Register enabled tests here
        self.registry.append(SchemaDocsSyncTest())
        # Future: self.registry.append(SomeOtherBenchmarkTest())

    def get_enabled_tests(self) -> list[unit_test_abstract.UnitTestInterface]:
        return self.registry