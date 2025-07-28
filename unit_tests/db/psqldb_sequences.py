# File: db/psqldb_sequences.py

from db.core.connection import get_db_connection


def get_sequence_mismatches() -> list[dict]:
    """
    Returns a list of sequences where last_value < MAX(id)+1,
    indicating a mismatch between the sequence and actual data.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    s.relname AS sequence_name,
                    t.relname AS table_name,
                    a.attname AS column_name,
                    seq.last_value
                FROM pg_class s
                JOIN pg_depend d ON d.objid = s.oid
                JOIN pg_class t ON d.refobjid = t.oid
                JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = d.refobjsubid
                JOIN pg_sequences seq ON seq.schemaname = 'public' AND seq.sequencename = s.relname
                WHERE s.relkind = 'S'
            """)
            sequences = cur.fetchall()

            mismatches = []

            for seq_name, table_name, column_name, last_value in sequences:
                cur.execute(f"SELECT MAX({column_name}) FROM {table_name}")
                max_id = cur.fetchone()[0]
                if max_id is not None and last_value is not None and last_value < (max_id + 1):
                    mismatches.append({
                        "sequence_name": seq_name,
                        "table_name": table_name,
                        "column_name": column_name,
                        "last_value": last_value,
                        "expected_min": max_id + 1
                    })

    finally:
        conn.close()

    return mismatches