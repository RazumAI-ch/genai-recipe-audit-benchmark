# File: unit_tests/run_all_benchmark_tests.py

from unit_tests.benchmark_tests.benchmark_test_factory import BenchmarkUnitTestFactory
from loggers.implementations.benchmark_unit_test_log_manager import BenchmarkUnitTestLogManager
import traceback


def run_all_benchmark_unit_tests():
    """
    Executes all enabled benchmark unit tests and logs output to individual files.
    """
    logger = BenchmarkUnitTestLogManager()
    test_factory = BenchmarkUnitTestFactory()
    tests = test_factory.get_enabled_tests()

    if not tests:
        print("No benchmark unit tests are currently enabled.")
        return

    for test in tests:
        log_path = logger.get_log_path(test.KEY)
        with open(log_path, "w") as log_file:
            try:
                print(f"Running test: {test.KEY}")
                test.run()
                log_file.write(f"[PASS] {test.KEY}\n")
                print(f"  PASS")
            except Exception as e:
                log_file.write(f"[FAIL] {test.KEY}\n")
                log_file.write(traceback.format_exc())
                print(f"  FAIL — see log: {log_path}")
                raise RuntimeError(f"Unit test '{test.KEY}' failed. See log: {log_path}")


if __name__ == "__main__":
    run_all_benchmark_unit_tests()