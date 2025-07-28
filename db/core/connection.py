import os

import psycopg2


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
