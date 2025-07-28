from typing import Optional

from db.core.connection import get_db_connection


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
