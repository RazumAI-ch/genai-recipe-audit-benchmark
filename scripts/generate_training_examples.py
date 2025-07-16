# File: scripts/generate_training_examples.py

import os
import json
import random
import csv
import io
import psycopg2
from datetime import datetime

# === Config ===
NUM_RECORDS = 10000
DB_CONFIG = dict(
    host=os.getenv("DB_HOST", "db"),  # "db" = Docker Compose service name
    dbname=os.getenv("DB_NAME", "benchmarkdb"),
    user=os.getenv("DB_USER", "benchmark"),
    password=os.getenv("DB_PASSWORD", "benchmark"),
    port=os.getenv("DB_PORT", "5432")
)

# === Helpers ===
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def json_to_csv(record: dict) -> str:
    flat = flatten_dict(record)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=flat.keys())
    writer.writeheader()
    writer.writerow(flat)
    return output.getvalue().strip()

def generate_record(i):
    return {
        "step_id": f"STEP_{i+1}",
        "description": f"Add solution to vessel {i+1}",
        "timestamp": f"2025-07-12T08:{i % 60:02d}:00Z",
        "operator": f"user_{i % 5}",
        "volume_ml": random.randint(100, 500)
    }

def fake_explanation(deviation_type_id, record_idx):
    return f"Artificially injected {deviation_type_id} deviation in sample {record_idx + 1}."

def infer_source_field(deviation_type_id):
    # Fake mapping for test data — adjust for real logic later
    if "timestamp" in deviation_type_id.lower():
        return "timestamp"
    elif "operator" in deviation_type_id.lower():
        return "operator"
    elif "volume" in deviation_type_id.lower():
        return "volume_ml"
    else:
        return "description"

# === Main Process ===
def main():
    print("Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 1. Load all deviation types
    cur.execute("SELECT id FROM deviation_types")
    deviation_ids = [row[0] for row in cur.fetchall()]
    if not deviation_ids:
        raise Exception("No deviation types found in database.")

    print(f"Generating {NUM_RECORDS} training examples...")

    for i in range(NUM_RECORDS):
        deviation_id = random.choice(deviation_ids)
        record = generate_record(i)
        input_format = "json" if i % 2 == 0 else "csv"
        input_content = json.dumps(record, ensure_ascii=False) if input_format == "json" else json_to_csv(record)

        # 2. Insert training example
        cur.execute("""
            INSERT INTO training_examples (input_format, input_content)
            VALUES (%s, %s)
            RETURNING id;
        """, (input_format, input_content))
        training_example_id = cur.fetchone()[0]

        # 3. Insert linked deviation
        explanation = None
        source_field = infer_source_field(deviation_id)

        cur.execute("""
            INSERT INTO training_example_deviations (training_example_id, deviation_type_id, explanation, source_field)
            VALUES (%s, %s, %s, %s);
        """, (training_example_id, deviation_id, explanation, source_field))

        if (i + 1) % 100 == 0:
            print(f"Inserted {i + 1} examples...")

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Done: {NUM_RECORDS} training examples inserted into database.")

if __name__ == "__main__":
    main()