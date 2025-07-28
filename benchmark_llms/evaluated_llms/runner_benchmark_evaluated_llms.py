# File: benchmark_llms/runner_benchmark_evaluated_llms.py

import db.database
from benchmark_llms.evaluated_llms.factory_evaluated_llms import FactoryEvaluatedLLMs


class RunnerBenchmarkEvaluatedLLMs:
    """
    Responsible for orchestrating the benchmark run using the factory.
    Loads sample records and evaluates them using all enabled models.
    """

    def __init__(self):
        self.factory = FactoryEvaluatedLLMs()

    def run_benchmark(self, max_records: int = None) -> None:
        sample_records = db.database.load_sample_records(limit=max_records)
        total_records = len(sample_records)

        for model_name, model_class in self.factory.get_enabled_models().items():
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