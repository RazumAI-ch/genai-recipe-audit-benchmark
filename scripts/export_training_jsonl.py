# File: scripts/export_training_jsonl.py

import os
import json
import psycopg2
import pandas as pd
from datetime import datetime

# === DB Connection ===
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),  # use "localhost" if running locally
    "dbname": os.getenv("DB_NAME", "benchmarkdb"),
    "user": os.getenv("DB_USER", "benchmark"),
    "password": os.getenv("DB_PASSWORD", "benchmark"),
    "port": os.getenv("DB_PORT", "5432")
}

def make_prompt(fmt, content, deviation_type, explanation):
    return f"""### Record Format: {fmt.upper()}

{content}

### Deviation Detected:
- ID: {deviation_type}
- Explanation: {explanation}
"""

def main():
    print("📦 Connecting to DB...")
    conn = psycopg2.connect(**DB_CONFIG)
    query = """
        SELECT te.input_format,
               te.input_content,
               td.deviation_type_id,
               td.explanation
        FROM training_examples te
        JOIN training_example_deviations td ON te.id = td.training_example_id
        ORDER BY te.id;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"📝 Exporting {len(df)} records...")

    df["prompt"] = df.apply(lambda row: make_prompt(
        row["input_format"],
        row["input_content"],
        row["deviation_type_id"],
        row["explanation"]
    ), axis=1)
    df["response"] = "### END"

    os.makedirs("training_data", exist_ok=True)
    filename = f"training_data/training_export_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.jsonl"

    with open(filename, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            json.dump({"prompt": row["prompt"], "response": row["response"]}, f)
            f.write("\n")

    print(f"✅ Exported training data to {filename}")

if __name__ == "__main__":
    main()