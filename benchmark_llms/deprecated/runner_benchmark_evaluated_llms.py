# File: benchmark_llms/runner_benchmark_evaluated_llms.py

import db.utils.load_sample_records
from benchmark_llms.deprecated.utils.factory_evaluated_llms import FactoryEvaluatedLLMs
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager
from concurrent.futures import ThreadPoolExecutor

class RunnerBenchmarkEvaluatedLLMs:
    """
    Responsible for orchestrating the benchmark run using the factory.
    Loads sample records and evaluates them using all enabled models in parallel.
    """

    def __init__(self):
        self.factory = FactoryEvaluatedLLMs()
        self.logger = BenchmarkLogFileManager("_benchmark_runner")

    def _run_single_model(self, model_name, model_class, sample_records):
        """
        Runs the benchmark for a single model. This method is called by each thread.
        """
        total_records = len(sample_records)
        print(f"\nLoading model: {model_name}")
        model = model_class()

        try:
            model.prepare()
            print(f"[{model_name}] Sending {total_records} records for audit...")
            model_output = model.evaluate(sample_records)
        except Exception as e:
            print(f"[{model_name}] Evaluation failed: {e}")
            return  # Exit this thread on failure

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

    def run_benchmark(self, max_records: int = None) -> None:
        """
        Loads sample records once, then evaluates all models in parallel using threads.
        """
        sample_records = db.utils.load_sample_records.load_sample_records(limit=max_records)
        enabled_models = self.factory.get_enabled_models()

        print(f"Starting parallel benchmark for {len(enabled_models)} models...")

        # Use a ThreadPoolExecutor to run the benchmarks in parallel
        with ThreadPoolExecutor() as executor:
            # Submit each model's benchmark to the thread pool
            futures = [
                executor.submit(self._run_single_model, model_name, model_class, sample_records)
                for model_name, model_class in enabled_models.items()
            ]

            # The 'with' block implicitly waits for all submitted futures to complete
            # before exiting.

        print("All benchmark runs have completed.")