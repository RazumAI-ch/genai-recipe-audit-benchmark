# File: main.py

import sys
from benchmark_llms.evaluated_llms.runner_benchmark_evaluated_llm import BenchmarkEvaluatedLLMRunner

def run_benchmark(max_records):
    # factory = EvaluatedLLMFactory()
    # factory.run_benchmark(max_records=max_records)

    runner = BenchmarkEvaluatedLLMRunner()
    runner.run_benchmark(max_records=max_records)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the GenAI Recipe Audit Benchmark")
    parser.add_argument("max_records", nargs="?", default="15",
                        help="Number of records to audit (e.g., 100, 1000, or 'none' for all records)")
    args = parser.parse_args()

    try:
        max_records = None if args.max_records.lower() == "none" else int(args.max_records)
    except ValueError:
        print("Invalid input for max_records. Use an integer or 'none'.")
        sys.exit(1)

    run_benchmark(max_records)