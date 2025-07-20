# File: llms/interface.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml

class LLMInterface(ABC):
    """
    Abstract interface for all LLM implementations.
    Handles config loading and enforces prepare + batch eval contract.
    """

    def __init__(self, config_path: str):
        self.model_config = self._load_config(config_path)

    def _load_config(self, path: str) -> dict:
        """
        Load model configuration from a YAML file.
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @abstractmethod
    def prepare(self, overrides: Dict[str, Any] = None) -> None:
        """
        Prepares the model for use (e.g., loads keys, prompts, starts containers).
        Allows optional runtime overrides (e.g., model version or batch size).
        """
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