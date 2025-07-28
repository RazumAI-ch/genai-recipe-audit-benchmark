# File: unit_tests/db/schema_docs.py

from db.database import get_db_connection

def get_all_columns() -> set[tuple[str, str]]:
    """
    Returns all (table_name, column_name) pairs from the actual PostgreSQL schema,
    lowercased for consistency.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT LOWER(table_name), LOWER(column_name)
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name NOT LIKE 'pg_%'
                AND table_name NOT LIKE 'sql_%'
            """)
            rows = cur.fetchall()
    finally:
        conn.close()

    return set((row[0], row[1]) for row in rows)


def get_documented_columns() -> set[tuple[str, str]]:
    """
    Returns all (table_name, column_name) pairs from schema_docs,
    lowercased for consistency.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT LOWER(table_name), LOWER(column_name)
                FROM schema_docs
            """)
            rows = cur.fetchall()
    finally:
        conn.close()

    return set((row[0], row[1]) for row in rows)