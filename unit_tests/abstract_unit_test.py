# File: unit_tests/abstract_unit_test.py

from abc import ABC, abstractmethod
from typing import ClassVar


class AbstractUnitTest(ABC):
    """
    Abstract base class for all unit tests.
    Implements shared exception handling wrapper for clean logs and readable errors.
    """

    KEY: ClassVar[str]

    @abstractmethod
    def run(self) -> None:
        """
        Subclasses must implement this. Should raise AssertionError or custom test failure exceptions.
        """
        pass

    def run_with_handling(self) -> None:
        """
        Calls self.run() and handles exceptions in a clean, uniform way.
        Should be called by the test runner instead of run().
        """
        try:
            self.run()
        except AssertionError as e:
            raise RuntimeError(f"[{self.KEY}] Assertion failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"[{self.KEY}] Unexpected error: {type(e).__name__}: {str(e)}")