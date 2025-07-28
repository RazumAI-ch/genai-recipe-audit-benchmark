# File: benchmark_llms/factory_evaluated_llm.py

import typing
import db.database
import config.keys
from benchmark_llms.evaluated_llms.implementations.model_openai import OpenAIModel

# Define which models are currently enabled for evaluation
ENABLED_MODELS = config.keys.ENABLED_BENCHMARK_MODELS

# Registry of all known models mapped to their implementation class
MODEL_REGISTRY = {
    OpenAIModel.get_model_key(): OpenAIModel,
    # config.keys.OPENAI_GPT_4: model_openai.OpenAIModel,
    # config.keys.CLAUDE_OPUS: model_claude.ClaudeModel,
    # config.keys.GEMINI_1_5_PRO: model_gemini.GeminiModel,
}


class EvaluatedLLMFactory:
    """
    Factory class responsible for registering and running all enabled benchmark_llms LLMs.
    """

    def __init__(self):
        self.model_registry = MODEL_REGISTRY
        self.enabled_models = ENABLED_MODELS

    def get_enabled_models(self) -> typing.Dict[str, typing.Type]:
        """
        Returns a filtered version of the model registry that includes only enabled models.
        """
        return {k: v for k, v in self.model_registry.items() if k in self.enabled_models}

    def load_model(self, model_name: str, overrides: typing.Dict[str, typing.Any] = None):
        """
        Instantiate a model class from the registry using the given name.
        Applies optional overrides (e.g., to change model version or batch size).
        """
        model_class = self.model_registry.get(model_name)
        if not model_class:
            raise ValueError(f"Model '{model_name}' is not registered.")
        model = model_class()
        model.prepare(overrides=overrides)
        return model
