# File: unit_tests/runner_unit_tests.py

from unit_tests.factory_unit_tests import FactoryUnitTests
from loggers.implementations.benchmark_unit_test_log_manager import BenchmarkUnitTestLogFileManager
from unit_tests.interface_unit_test import UnitTestInterface
import traceback


def run_all_benchmark_unit_tests():
    """
    Executes all enabled benchmark unit tests and logs output to individual files.
    """
    logger = BenchmarkUnitTestLogFileManager()
    unit_test_factory = FactoryUnitTests()
    enabled_unit_tests = unit_test_factory.get_enabled_tests()

    if not enabled_unit_tests:
        print("No benchmark unit tests are currently enabled.")
        return

    for unit_test in enabled_unit_tests:
        unit_test: UnitTestInterface = unit_test  # Explicit cast for clarity
        initial_log_msg = f"Running unit test: {unit_test.KEY}\n"
        log_path = logger.write_log(suffix=unit_test.KEY, content=initial_log_msg)

        def log(message: str):
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")

        try:
            unit_test.run()
            log(f"[PASS] {unit_test.KEY}")
        except Exception:
            log(f"[FAIL] {unit_test.KEY}")
            log(traceback.format_exc())
            raise RuntimeError(f"Unit test '{unit_test.KEY}' failed. See log: {log_path}")


if __name__ == "__main__":
    run_all_benchmark_unit_tests()