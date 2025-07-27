# File: main.py

import sys
import os
import json
import datetime
import pathlib

import db.database
import config.keys
import llms.factory

def run_benchmark(max_records):
    sample_records = db.database.load_sample_records(limit=max_records)
    total_records = len(sample_records)

    for model_name, model_class in llms.factory.get_enabled_models().items():
        print(f"\nLoading model: {model_name}")
        model = model_class()
        model.prepare()

        print(f"Sending {total_records} records for audit...")
        try:
            model_output = model.evaluate(sample_records)
        except Exception as e:
            print("Evaluation failed:", e)
            continue

        records = model_output.get("records", [])
        with_issues = [r for r in records if r.get("deviations")]

        print(f"\nSummary for {model_name}: {len(records)} records audited. {len(with_issues)} had deviations.\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the GenAI Recipe Audit Benchmark")
    parser.add_argument("max_records", nargs="?", default="10",
                        help="Number of records to audit (e.g., 100, 1000, or 'none' for all records)")
    args = parser.parse_args()

    try:
        max_records = None if args.max_records.lower() == "none" else int(args.max_records)
    except ValueError:
        print("Invalid input for max_records. Use an integer or 'none'.")
        sys.exit(1)

    run_benchmark(max_records)