# File: benchmark/factory_evaluated_llm.py

import typing
import db.database
import benchmark.config.keys
from benchmark.evaluated_llms.implementations.model_openai import OpenAIModel

# Define which models are currently enabled for evaluation
ENABLED_MODELS = benchmark.config.keys.ENABLED_BENCHMARK_MODELS

# Registry of all known models mapped to their implementation class
MODEL_REGISTRY = {
    OpenAIModel.get_model_key(): OpenAIModel,
    # config.keys.OPENAI_GPT_4: model_openai.OpenAIModel,
    # config.keys.CLAUDE_OPUS: model_claude.ClaudeModel,
    # config.keys.GEMINI_1_5_PRO: model_gemini.GeminiModel,
}


class EvaluatedLLMFactory:
    """
    Factory class responsible for registering and running all enabled benchmark LLMs.
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

    def run_benchmark(self, max_records: int = None):
        """
        Loads sample records and evaluates them using all enabled models.
        Prints a summary of the results for each model.
        """
        sample_records = db.database.load_sample_records(limit=max_records)
        total_records = len(sample_records)

        for model_name, model_class in self.get_enabled_models().items():
            print(f"\nLoading model: {model_name}")
            model = model_class()

            try:
                model.prepare()
                print(f"Sending {total_records} records for audit...")
                model_output = model.evaluate(sample_records)
            except Exception as e:
                print(f"Evaluation failed for {model_name}: {e}")
                continue

            audited_records = model_output.get("records", [])
            records_with_deviations = [r for r in audited_records if r.get("deviations")]

            print(f"Summary for {model_name}:")
            print(f"- Records sent for audit: {total_records}")
            print(f"- Records with deviations: {len(records_with_deviations)}\n")