# File: unit_tests/benchmark_tests/benchmark_test_factory.py

from unit_tests.unit_test_factory_abstract import UnitTestFactoryAbstract
# from unit_tests.benchmark_tests.core.test_schema_sync import SchemaDocsSyncTest

class BenchmarkUnitTestFactory(UnitTestFactoryAbstract):
    """
    Concrete factory that registers all unit tests relevant to the benchmark_llms pipeline.
    Provides a list of enabled test instances implementing UnitTestInterface.
    """

    # Enable test keys by default (add when implemented)
    ENABLED_UNIT_TESTS = set()

    # Registry of available tests (key → class)
    UNIT_TEST_REGISTRY = {
        # "schema_docs_sync": SchemaDocsSyncTest,
    }