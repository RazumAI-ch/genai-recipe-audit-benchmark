# File: benchmark_llms/utils/runner_benchmark_evaluated_llms_from_models_yaml.py

from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager
from benchmark_llms.evaluated_llms.factory_evaluated_llms_from_models_yaml import (
    FactoryEvaluatedLLMsFromModelsYAML,
)


class RunnerBenchmarkEvaluatedLLMsFromModelsYAML:
    """
    MC1 runner (models.yaml-driven).
    For the first milestone, we DO NOT run inference.
    """

    def __init__(self):
        print("DEBUG: RunnerBenchmarkEvaluatedLLMsFromModelsYAML.__init__ starting")
        self.factory = FactoryEvaluatedLLMsFromModelsYAML()
        print("DEBUG: FactoryEvaluatedLLMsFromModelsYAML instantiated")
        self.logger = BenchmarkLogFileManager("_benchmark_runner_models_yaml")
        print("DEBUG: RunnerBenchmarkEvaluatedLLMsFromModelsYAML.__init__ complete")

    def run_benchmark(self, max_records: int = None) -> None:
        print("DEBUG: run_benchmark called")

        # Discover enabled models from models.yaml
        enabled = self.factory.get_enabled_models()
        print(f"DEBUG: get_enabled_models returned {len(enabled)} models")

        model_keys = list(enabled.keys())
        print(f"DEBUG: model_keys = {model_keys}")

        print("\n[models.yaml] Discovered enabled models:")
        for k in model_keys:
            cfg = enabled[k]
            print(
                f"  - {k} | provider={cfg.get('provider')} "
                f"model={cfg.get('model')} "
                f"temp={cfg.get('temperature')} "
                f"max_tokens={cfg.get('max_tokens')} "
                f"batch_size={cfg.get('batch_size')} "
                f"enabled={cfg.get('enabled', True)}"
            )

        self.logger.write_log(
            "mc1_discovery",
            {
                "enabled_model_keys": model_keys,
                "enabled_models_resolved": enabled,
            },
        )

        # Try instantiating each model via the MC1 factory (no inference yet)
        instantiated = []
        for k in model_keys:
            try:
                print(f"DEBUG: Attempting to load model {k}")
                model = self.factory.load_model(k)  # prepare() happens inside load_model()
                instantiated.append(model.__class__.__name__)
                print(f"[models.yaml] Instantiated: {k} -> {model}")
            except Exception as e:
                print(f"[models.yaml] FAILED to instantiate {k}: {e}")

        self.logger.write_log(
            "mc1_instantiation",
            {
                "instantiated_count": len(instantiated),
                "instantiated_classes": instantiated,
            },
        )

        print(
            "\n[models.yaml] MC1 wiring OK. "
            "Config merged, models instantiated (no inference yet)."
        )