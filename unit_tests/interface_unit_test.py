# File: interface_unit_test.py

"""
This interface defines the contract for any individual unit test used in the
benchmark_llms or llm_training workflows.

All unit test implementations must inherit from this class and implement the `run()` method.

This approach ensures that each unit test:
- Can be executed via a standardized interface
- Is discoverable and runnable via a central factory
- Remains decoupled from specific runner logic

Each test is expected to raise an Exception or AssertionError on failure.
"""

import typing
from abc import ABC, abstractmethod

class UnitTestInterface(ABC):
    """
    All unit tests must inherit from this interface.
    They must define a KEY class variable used for registration.
    """
    KEY: typing.ClassVar[str]

    @abstractmethod
    def run(self) -> None:
        """
        Executes the unit test.

        Raises:
            AssertionError or custom exceptions if the test fails.
        """
        pass