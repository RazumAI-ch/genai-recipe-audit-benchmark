import os
import psycopg2
import random
import json
from datetime import datetime

# Config
LLM_ID = 1  # Replace with actual ChatGPT LLM ID
SAMPLE_COUNT = 100

conn = psycopg2.connect(
    host="localhost",
    dbname="benchmarkdb",
    user="benchmark",
    password="benchmark"
)
cur = conn.cursor()

# Step 1: create benchmark run
run_name = "baseline-chatgpt-001"
cur.execute("INSERT INTO benchmark_runs (run_name, sample_size) VALUES (%s, %s) RETURNING id;", (run_name, SAMPLE_COUNT))
run_id = cur.fetchone()[0]

# Step 2: load all deviation types
cur.execute("SELECT id FROM deviation_types")
deviation_ids = [row[0] for row in cur.fetchall()]

# Step 3: generate 100 records with deviations
for i in range(SAMPLE_COUNT):
    content = {
        "step_id": f"STEP_{i+1}",
        "description": f"Add solution to vessel {i+1}",
        "timestamp": f"2025-07-12T08:{i%60:02d}:00Z",
        "operator": f"user_{i%5}",
        "volume_ml": random.randint(100, 500)
    }
    prompt_used = "Generate realistic manufacturing step JSON"

    # Insert sample record
    cur.execute("""
        INSERT INTO sample_records (run_id, llm_id, content, generation_prompt)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (run_id, LLM_ID, json.dumps(content), prompt_used))
    sample_id = cur.fetchone()[0]

    # Randomly pick 1–3 deviations
    picked = random.sample(deviation_ids, k=random.randint(1, 3))

    # Insert into deviations and build injected_deviation_ids
    for deviation_type_id in picked:
        cur.execute("""
            INSERT INTO deviations (sample_record_id, deviation_type_id)
            VALUES (%s, %s);
        """, (sample_id, deviation_type_id))

    cur.execute("""
        UPDATE sample_records
        SET injected_deviation_ids = %s
        WHERE id = %s;
    """, (picked, sample_id))

conn.commit()
cur.close()
conn.close()
print("✅ Inserted 100 sample records with deviations.")