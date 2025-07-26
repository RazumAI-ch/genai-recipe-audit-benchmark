# File: scripts/export_sample_records.py

import os
import json
import psycopg2

OUTPUT_PATH = "public_assets/exported_sample_records.json"

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "benchmarkdb"),
    user=os.getenv("POSTGRES_USER", "benchmark"),
    password=os.getenv("POSTGRES_PASSWORD", "benchmark"),
    host=os.getenv("POSTGRES_HOST", "localhost"),  # or "db" if run inside Docker
    port=os.getenv("POSTGRES_PORT", "5432")
)

with conn.cursor() as cur:
    cur.execute("SELECT id, content FROM sample_records ORDER BY id;")
    rows = cur.fetchall()

conn.close()

records = [{"id": str(row[0]), **row[1]} for row in rows]

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

print(f"✅ Exported {len(records)} records to {OUTPUT_PATH}")