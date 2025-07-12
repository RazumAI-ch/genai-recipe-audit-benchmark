# File: main.py

from dotenv import load_dotenv
from llms.model_openai import OpenAIModel

load_dotenv()

def main():
    print("🚀 GenAI Recipe Audit Benchmark: Starting test run...")

    # Create and prepare the model (loads config internally)
    model = OpenAIModel()
    model.prepare()

    # Dummy records (normally these come from the DB)
    records = [
        {"id": 1, "content": {"step_id": "S1", "description": "Add buffer", "operator": "user1"}},
        {"id": 2, "content": {"step_id": "S2", "description": "Heat to 70C", "operator": "user2"}},
    ]

    results = model.evaluate_batch(records)

    for r in results:
        print("\nRecord ID:", r["sample_record_id"])
        print("Detected deviations:", r["detected_deviation_ids"])

if __name__ == "__main__":
    main()