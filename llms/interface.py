# File: llms/interface.py

from abc import ABC, abstractmethod
from typing import List, Dict
import yaml

class LLMInterface(ABC):
    """
    Abstract interface for all LLM implementations.
    Handles config loading and enforces prepare + batch eval contract.
    """

    def __init__(self, config_path: str):
        self.model_config = self._load_config(config_path)

    def _load_config(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @abstractmethod
    def prepare(self):
        """
        Prepares the model for use (e.g., loads keys, prompts, starts containers).
        """
        pass

    @abstractmethod
    def evaluate_batch(self, records: List[Dict]) -> List[Dict]:
        """
        Evaluate a batch of records and return list of results per record.
        """
        pass