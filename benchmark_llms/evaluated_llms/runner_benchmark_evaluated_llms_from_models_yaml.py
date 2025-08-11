# File: benchmark_llms/utils/runner_benchmark_evaluated_llms_from_models_yaml.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager
from benchmark_llms.evaluated_llms.factory_evaluated_llms_from_models_yaml import (
    FactoryEvaluatedLLMsFromModelsYAML,
)


class RunnerBenchmarkEvaluatedLLMsFromModelsYAML:
    """
    MC1 runner (models.yaml-driven).

    What this does now:
      1) Loads and prints enabled models from models.yaml
      2) Instantiates each model via FactoryEvaluatedLLMsFromModelsYAML (prepare() runs)
      3) (NEW) Performs a tiny smoke inference per model and prints the raw provider response

    Notes:
      - We call the model's private `_run_model_inference` to keep parity with legacy,
        since public `run()` may vary by implementation. Replace with a public
        method once the MC1 interface is finalized.
    """

    def __init__(self, *, do_inference: bool = True):
        print("DEBUG: RunnerBenchmarkEvaluatedLLMsFromModelsYAML.__init__ starting")
        self.factory = FactoryEvaluatedLLMsFromModelsYAML()
        print("DEBUG: FactoryEvaluatedLLMsFromModelsYAML instantiated")
        self.logger = BenchmarkLogFileManager("_benchmark_runner_models_yaml")
        self.do_inference = do_inference
        print("DEBUG: RunnerBenchmarkEvaluatedLLMsFromModelsYAML.__init__ complete")

    def _demo_records(self, n: int = 1) -> List[Dict[str, Any]]:
        """
        Minimal demo records compatible with our prompt templates.
        Adjust the schema as your prompts expect.
        """
        out = []
        for i in range(n):
            out.append(
                {
                    "id": f"demo-{i+1}",
                    "text": "Hello from MC1 smoke test.",
                }
            )
        return out

    def run_benchmark(self, max_records: Optional[int] = None) -> None:
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

        # Instantiate & (optionally) run a tiny inference per model
        instantiated = []
        inference_ok = []
        inference_fail = []

        for k in model_keys:
            try:
                print(f"DEBUG: Attempting to load model {k}")
                model = self.factory.load_model(k)  # prepare() happens inside
                instantiated.append(model.__class__.__name__)
                print(f"[models.yaml] Instantiated: {k} -> {model}")
            except Exception as e:
                print(f"[models.yaml] FAILED to instantiate {k}: {e}")
                continue

            if not self.do_inference:
                continue

            # Smoke inference with 1 record unless caller overrides
            n = max_records if (isinstance(max_records, int) and max_records > 0) else 1
            records = self._demo_records(n)

            try:
                raw = model._run_model_inference(records)  # intentionally private for now
                print(f"[models.yaml] Raw provider response for {k}: {raw}")
                inference_ok.append(k)
            except Exception as e:
                print(f"[models.yaml] Inference failed for {k}: {e}")
                inference_fail.append({"model_key": k, "error": str(e)})

        # Logging summary
        self.logger.write_log(
            "mc1_instantiation",
            {"instantiated_count": len(instantiated), "instantiated_classes": instantiated},
        )
        if self.do_inference:
            self.logger.write_log(
                "mc1_inference",
                {"ok": inference_ok, "fail": inference_fail},
            )

        tail = "with smoke inference." if self.do_inference else " (no inference)."
        print(f"\n[models.yaml] MC1 wiring OK. Config merged, models instantiated {tail}")