# File: main.py

import sys
import argparse

from benchmark_llms.utils.runner_benchmark_evaluated_llms import (
    RunnerBenchmarkEvaluatedLLMs,
)
from benchmark_llms.utils.runner_benchmark_evaluated_llms_from_models_yaml import (
    RunnerBenchmarkEvaluatedLLMsFromModelsYAML,
)


def run_legacy(max_records):
    print("\n[legacy] Running legacy benchmark (folder-scanned implementations)...")
    runner = RunnerBenchmarkEvaluatedLLMs()
    runner.run_benchmark(max_records=max_records)


def run_from_models_yaml(max_records):
    print("\n[models.yaml] Running models.yaml–driven benchmark...")
    runner = RunnerBenchmarkEvaluatedLLMsFromModelsYAML()
    runner.run_benchmark(max_records=max_records)


if __name__ == "__main__":
    # Keep the interface exactly as before: one optional positional arg.
    parser = argparse.ArgumentParser(
        description="GenAI Recipe Audit Benchmark (legacy default run)"
    )
    parser.add_argument(
        "max_records",
        nargs="?",
        default="15",
        help="Number of records to audit (e.g., 1, 50, 1000, or 'none' for all records)",
    )
    args = parser.parse_args()

    try:
        max_records = None if str(args.max_records).lower() == "none" else int(args.max_records)
    except ValueError:
        print("Invalid input for max_records. Use an integer or 'none'.")
        sys.exit(1)

    # Default behavior: run legacy only (exactly like before).
    run_legacy(max_records)

    # ----------------------------------------------------------------------
    # To test the models.yaml path, just uncomment the two lines below.
    # ----------------------------------------------------------------------
    print("\n[main] Note: Running models.yaml path after legacy (manual toggle).")
    run_from_models_yaml(max_records)