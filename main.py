# File: main.py

import json
from pathlib import Path
from llms.factory import load_model
from config.keys import OPENAI_GPT_4O

# 🔧 List of models to benchmark (can be extended with more model keys)
MODEL_LIST = [
    OPENAI_GPT_4O,  # For now, benchmarking only GPT-4o
]

# 📄 Load the first 10 records from test_data.json
def load_sample_records(filepath: str, count: int = 99) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [{"id": i + 1, "content": record} for i, record in enumerate(data[:count])]

def run_benchmark():
    """
    Main benchmarking loop.
    Loads and prepares each model from MODEL_LIST,
    evaluates a batch of sample records,
    and prints the result count (DB integration to follow).
    """
    sample_records = load_sample_records("public_assets/test_data.json", count=100)

    for model_name in MODEL_LIST:
        print(f"\n🚀 Loading model: {model_name}")
        model = load_model(model_name)  # Load and prepare the model instance

        print("🔍 Sending records for full-batch audit...")
        results = model.evaluate_batch(sample_records)

        print(f"✅ Evaluation complete for {model_name}. {len(results)} records evaluated.")
        print("\n📤 Structured audit results:")
        for res in results:
            print(res)

# 🏁 Entry point when running this script directly
if __name__ == "__main__":
    run_benchmark()