# File: benchmark_llms/interface_evaluated_llm.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml
import config.paths as config_paths

class InterfaceEvaluatedLLM(ABC):
    """
    Abstract interface for all LLM implementations.
    Handles config loading and enforces prepare + batch eval contract.
    """

    # =======================================================================
    # REQUIRED_STATIC_FIELD
    # -----------------------------------------------------------------------
    # This constant defines the required static class variable that all
    # final LLM implementations must declare locally in their class body.
    #
    # It is used by the model discovery system (factory_evaluated_llms.py)
    # to:
    #   - Identify which classes are final, concrete implementations
    #   - Avoid registering abstract or intermediate base classes
    #   - Enforce an explicit contract for model identity
    #
    # Why it's needed:
    # - Python provides no clean way to mark a class as "final"
    # - Python's ABC machinery does not apply to static class variables
    # - `inspect.isabstract(cls)` is unreliable without forcing dummy abstract methods
    # - `hasattr(cls, 'ModelKey')` includes inherited fields, which breaks discovery
    #
    # Instead, we check:
    #     if InterfaceEvaluatedLLM.REQUIRED_STATIC_FIELD in cls.__dict__
    #
    # This ensures only classes that define ModelKey *directly* are registered.
    #
    # IMPORTANT:
    # If you ever rename 'ModelKey', you must update this constant
    # (and refactor its usage in the factory loader).
    # =======================================================================
    REQUIRED_STATIC_FIELD = "ModelKey"

    # Static identifier for each final model implementation.
    ModelKey: str

    @abstractmethod
    def prepare(self, overrides: Dict[str, Any] = None) -> None:
        """
        Prepares the model for use (e.g., loads keys, prompts, starts containers).
        Allows optional runtime overrides (e.g., model version or batch size).
        """
        pass


    @classmethod
    @abstractmethod
    def get_model_key(cls) -> str:
        pass


    @abstractmethod
    def evaluate(self, records: List[Dict], context_prefix: str = "") -> List[Dict]:
        """
        Evaluate a batch of records and return list of results per record.

        Parameters:
        - records: list of input records, each a dictionary with required keys.
        - context_prefix: optional string prepended to the prompt for additional context
                          (e.g., known deviation types, examples, instructions).

        Returns:
        - A list of dictionaries with fields like sample_record_id, detected_deviation_ids, etc.
        """
        pass