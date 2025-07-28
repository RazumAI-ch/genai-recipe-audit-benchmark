# File: db/database.py

import psycopg2
import os
from typing import Optional


def get_db_connection():
    """
    Establish a PostgreSQL connection using environment variables.

    Environment variables expected (set via .env or Docker):
    - DB_HOST
    - POSTGRES_DB
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - DB_PORT

    Raises:
        RuntimeError if any required variable is missing.

    Returns:
        psycopg2 connection object
    """
    required_vars = ["DB_HOST", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "DB_PORT"]
    missing = [var for var in required_vars if os.getenv(var) is None]
    if missing:
        raise RuntimeError(f"Missing required DB environment variables: {', '.join(missing)}")

    db_config = {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "port": os.getenv("DB_PORT"),
    }

    return psycopg2.connect(**db_config)


def load_sample_records(source_filter: Optional[str] = None, limit: Optional[int] = None) -> list[dict]:
    """
    Loads records from the sample_records table, optionally filtered and randomly sampled.

    Args:
        source_filter: Optional source string to filter by sample_records.source
        limit: Optional int to randomly select a subset of records

    Returns:
        List of JSON-style dicts with 'id' and all content fields.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT id, content FROM sample_records"
            params = []

            if source_filter:
                query += " WHERE source = %s"
                params.append(source_filter)

            query += " ORDER BY RANDOM()"
            if limit:
                query += " LIMIT %s"
                params.append(limit)

            cur.execute(query, tuple(params))
            rows = cur.fetchall()
    finally:
        conn.close()

    return [{"id": str(row[0]), **row[1]} for row in rows]

