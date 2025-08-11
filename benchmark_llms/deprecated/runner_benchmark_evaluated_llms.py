# File: benchmark_llms/runner_benchmark_evaluated_llms.py

import db.utils.load_sample_records
from benchmark_llms.deprecated.utils.factory_evaluated_llms import FactoryEvaluatedLLMs
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager


class RunnerBenchmarkEvaluatedLLMs:
    """
    Responsible for orchestrating the benchmark run using the factory.
    Loads sample records and evaluates them using all enabled models.
    """

    def __init__(self):
        self.factory = FactoryEvaluatedLLMs()
        self.logger = BenchmarkLogFileManager("_benchmark_runner")

    def run_benchmark(self, max_records: int = None) -> None:
        sample_records = db.utils.load_sample_records.load_sample_records(limit=max_records)
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

            self.logger.write_log(
                suffix=f"{model_name}_summary",
                content={
                    "records_evaluated": total_records,
                    "records_with_deviations": len(records_with_deviations)
                }
            )

            print(f"Summary for {model_name}:")
            print(f"- Records sent for audit: {total_records}")
            print(f"- Records with deviations: {len(records_with_deviations)}\n")