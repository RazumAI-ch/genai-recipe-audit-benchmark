# File: db/database.py

import psycopg2
import os

def get_db_connection():
    """
    Establishes and returns a new connection to the PostgreSQL benchmark database.

    This function centralizes DB connection logic so that any part of the application
    needing DB access (training runs, benchmark logs, schema updates, etc.)
    can reuse this configuration. It reads connection parameters from environment
    variables to allow flexibility across local, Docker, or cloud deployments.

    Env vars used:
    - DB_HOST: the hostname of the database server (default: 'db' for Docker)
    - POSTGRES_DB: the name of the database to connect to (default: 'benchmarkdb')
    - POSTGRES_USER: the username for authentication (default: 'benchmark')
    - POSTGRES_PASSWORD: the user's password (default: 'benchmark')
    - DB_PORT: the port PostgreSQL is listening on (default: '5432')

    Returns:
        A live psycopg2 connection object, which must be manually closed by the caller.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("POSTGRES_DB", "benchmarkdb"),
        user=os.getenv("POSTGRES_USER", "benchmark"),
        password=os.getenv("POSTGRES_PASSWORD", "benchmark"),
        port=os.getenv("DB_PORT", "5432"),
    )