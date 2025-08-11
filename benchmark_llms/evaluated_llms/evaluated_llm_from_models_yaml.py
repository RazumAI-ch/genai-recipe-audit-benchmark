# File: benchmark_llms/evaluated_llms/evaluated_llm_from_models_yaml.py

from typing import Dict, Optional, List
from benchmark_llms.evaluated_llms.abstract_evaluated_llm_api_access import (
    AbstractEvaluatedLLM_APIAccess,
)
from config.keys_evaluated_llms import MODEL


class EvaluatedLLMFromModelsYAML(AbstractEvaluatedLLM_APIAccess):
    """
    MC1 (models.yaml-driven) evaluated LLM.
    Works exactly like a legacy evaluated LLM, except:
      - config comes from merged models.yaml instead of per-model YAML file
      - provider call is temporarily replaced by a debug print
    """

    def __init__(self, model_key: str, model_config: Dict):
        # Set the static ModelKey exactly as legacy expects
        type(self).ModelKey = model_key

        # Save merged config from factory so _load_config() can return it
        self._injected_model_config: Dict = dict(model_config)

        # Call the normal base class init — will trigger _load_config()
        super().__init__()

        # Handy shortcuts (also finalized in prepare())
        self.model = self.model_config.get(MODEL)
        self.batch_size = self.model_config.get("batch_size")
        self.temperature = self.model_config.get("temperature")
        self.max_tokens = self.model_config.get("max_tokens")

    # Return injected merged config instead of reading a per-model YAML file
    def _load_config(self, path: str) -> Dict:
        return self._injected_model_config

    @classmethod
    def get_model_key(cls) -> str:
        if not hasattr(cls, "ModelKey") or not cls.ModelKey:
            raise ValueError(f"{cls.__name__} must define a static 'ModelKey'.")
        return cls.ModelKey

    def prepare(self, overrides: Optional[Dict] = None):
        """
        Normal prepare flow — identical to legacy:
          - loads prompts
          - injects deviation section
          - appends timestamp
          - applies overrides
          - resolves API key from env var based on config
        """
        super().prepare(overrides=overrides)

    def _run_model_inference(self, records: List[Dict]) -> str:
        """
        For MC1 debug: print merged config and any other runtime attributes
        instead of actually calling the provider API.
        """
        print("\n[DEBUG] --- MC1 Inference Debug Info ---")
        print(f"ModelKey: {self.get_model_key()}")
        print(f"Provider: {self.model_config.get('provider')}")
        print(f"Model: {self.model}")

        # Print merged config from models.yaml
        print("\n[DEBUG] Merged config from models.yaml:")
        for k, v in self.model_config.items():
            print(f"  {k}: {v}")

        # Print any extra runtime attributes that aren’t in model_config
        extra_attrs = {
            k: v for k, v in self.__dict__.items()
            if k not in self.model_config and not k.startswith("_")
        }
        if extra_attrs:
            print("\n[DEBUG] Extra runtime attributes (not from models.yaml):")
            for k, v in extra_attrs.items():
                print(f"  {k}: {v}")
        else:
            print("\n[DEBUG] No extra runtime attributes found.")

        print("[DEBUG] --- End of MC1 Inference Debug Info ---\n")
        # Minimal valid JSON so downstream parse succeeds
        return '{"records": []}'

    def __repr__(self) -> str:
        return f"<EvaluatedLLMFromModelsYAML key={self.ModelKey} model={self.model}>"