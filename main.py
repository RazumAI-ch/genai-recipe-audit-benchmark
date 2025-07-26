# File: main.py

import sys
import os
import json
import psycopg2
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from llms.factory import load_model
from config.keys import OPENAI_GPT_4O

MODEL_LIST = [OPENAI_GPT_4O]

def load_sample_records_from_db() -> list[dict]:
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "benchmarkdb"),
            user=os.getenv("POSTGRES_USER", "benchmark"),
            password=os.getenv("POSTGRES_PASSWORD", "benchmark"),
            host=os.getenv("POSTGRES_HOST", "db"),  # 🔧 Use Docker Compose service name
            port=os.getenv("POSTGRES_PORT", "5432")
        )
    except Exception as e:
        print("❌ Failed to connect to the database:", e)
        raise

    with conn.cursor() as cur:
        cur.execute("SELECT id, content FROM sample_records ORDER BY id;")
        rows = cur.fetchall()
    conn.close()

    return [{"id": str(row[0]), **row[1]} for row in rows]

def run_benchmark():
    sample_records = load_sample_records_from_db()
    total_records = len(sample_records)

    for model_name in MODEL_LIST:
        print(f"\n🚀 Loading model: {model_name}")
        model = load_model(model_name)

        print("🔍 Sending records for full-batch audit...")
        model_output = model.evaluate(sample_records)

        records = model_output.get("records", [])
        total = len(records)
        with_issues = [r for r in records if r.get("deviations")]
        num_with_issues = len(with_issues)

        all_issues = []
        for rec in with_issues:
            all_issues.extend(rec["deviations"])

        critical = [i for i in all_issues if any(w in i["type"].lower() for w in ["missing", "invalid"])]
        moderate = [i for i in all_issues if any(w in i["type"].lower() for w in ["format", "incomplete", "non-standard"])]
        minor = [i for i in all_issues if i not in critical + moderate]

        print(f"""
📋 Healthcare Recipe Data Audit Report
Model: {model_name}
Audited Source: PostgreSQL sample_records table
Audit performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CEST

Executive Summary
The dataset contains several deviations, with a mix of critical, moderate, and minor issues.
- Overall Data Quality Score (1–10): {'6' if len(critical) >= 5 else '7'}
- Total entries in DB: {total_records}
- Total records audited: {total}
- Records with deviations: {num_with_issues}
- Records fully compliant: {total - num_with_issues}
- Compliance rate: {100 * (total - num_with_issues) / total:.1f}%
- Number of critical deviations: {len(critical)}
- Number of moderate deviations: {len(moderate)}
- Number of minor deviations: {len(minor)}

Most common critical deviations:
- Missing Data: {sum('missing' in i["type"].lower() for i in critical)}
- Invalid Status: {sum('invalid' in i["type"].lower() for i in critical)}

Most common moderate deviations:
- Format Error: {sum('format' in i["type"].lower() for i in moderate)}
- Inconsistency: {sum('inconsistent' in i["type"].lower() for i in moderate)}

**According to industry standards, records with critical findings should be remediated within 7 days, and records with moderate findings within 30 days.
""")

        print("Detailed Findings (first 5 records with deviations):")
        for rec in with_issues[:5]:
            print(f"\nRecord ID: {rec['id']}")
            for i in rec["deviations"]:
                issue = i.get("type", "—")
                severity = i.get("severity", "—")
                desc = i.get("description", "")
                print(f"- Deviation Type: {issue}\n  Severity: {severity}\n  Description: {desc}")

if __name__ == "__main__":
    run_benchmark()