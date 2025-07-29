# File: unit_tests/runner_unit_tests.py

from unit_tests.factory_unit_tests import FactoryUnitTests
from loggers.implementations.unit_test_log_manager import UnitTestLogFileManager
from unit_tests.abstract_unit_test import AbstractUnitTest
import config.paths as config_paths


class RunnerUnitTests:
    """
    Class responsible for executing all enabled unit tests and logging their results.
    """

    def __init__(self):
        self.factory = FactoryUnitTests()

    def run_all(self) -> None:
        enabled_unit_tests = self.factory.get_enabled_tests()

        if not enabled_unit_tests:
            print("No benchmark unit tests are currently enabled.")
            return

        for unit_test in enabled_unit_tests:
            unit_test: AbstractUnitTest = unit_test

            self.logger = UnitTestLogFileManager(context_folder_path=unit_test.LOG_FOLDER_PATH, subfolder_name=unit_test.KEY)

            initial_log_msg = f"Running unit test: {unit_test.KEY}\n"
            log_path = self.logger.write_log(suffix=unit_test.KEY, content=initial_log_msg)

            def log(message: str):
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(message + "\n")

            try:
                unit_test.run_with_handling()
                log(f"[PASS] {unit_test.KEY}")
            except Exception as e:
                log(f"[FAIL] {unit_test.KEY}")
                log(str(e))
                print(f"❌ Unit test '{unit_test.KEY}' failed.\n    See log: {log_path}")
                raise SystemExit(1)  # Exit cleanly with failure status


if __name__ == "__main__":
    try:
        RunnerUnitTests().run_all()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔍 Check if your imports match class renames and file structure.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        raise SystemExit(1)