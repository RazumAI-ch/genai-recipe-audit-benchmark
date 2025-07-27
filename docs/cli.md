# 🧰 Command-Line Interface (CLI) Guide – GenAI Recipe Audit Benchmark

This guide documents how to interact with the project via the command line, including:
- Starting/stopping the PostgreSQL container
- Resetting the database schema
- Loading LLM and deviation seeds
- Viewing table contents and database stats
- Running the benchmark

---

## Prerequisites

- Docker installed and available in your terminal
- `make` installed (comes preinstalled on macOS and Linux)
- Project cloned locally

---

## Project Commands via `make`

The project includes a `Makefile` with helpful shortcuts:

| Command                      | Description                                                   |
|------------------------------|---------------------------------------------------------------|
| `make wait-for-db`           | Wait for DB container to be ready before executing commands   |
| `make recreate_empty_db`     | Drop all containers and volumes, and restart everything        |
| `make fix-sequences`         | Reset Postgres sequences after restoring a backup             |
| `make refresh-schema-docs`   | Refresh schema.sql and update `schema_docs` with missing fields |
| `make sort-schema-docs`      | Sort `schema_docs` by table and column name                   |
| `make save_to_file`          | Save current DB state into a compressed `.sql.gz` file         |
| `make copy-latest-db-to-archive` | Copy most recent DB backup to `archive/` as `db-backup-latest.zip` |
| `make archive-latest-logs`   | Archive all training logs to `logs-latest.zip`                |
| `make import-db`             | Restore DB from latest archive                                |
| `make import-db-adhoc FILE=path/to/file.sql.gz` | Restore DB from a specified compressed file      |
| `make run`                   | Run the benchmark using `main.py`                             |
| `make show-db-stats`         | Show current row counts for all key tables                    |
| `make clear`                 | Clear the terminal                                            |

Run these from your project root, for example:

```bash
make save_to_file
make run
```

---

## Manual DB Interactions (Advanced)

### Load a SQL File
```bash
docker compose exec db psql -U benchmark -d benchmarkdb -f /app/db/some_script.sql
```

### Open psql Prompt
```bash
make psql
```

---

## See Also

- `README.md` – project overview
- `db/schema.sql` – core schema definition
- `db/refresh_schema_docs.sql` – autofill missing documentation entries
- `db/sort_schema_docs.sql` – keep schema_docs consistent and readable
- `archive/` – backups and logs
- `logs/debug/` – last model responses (auto overwritten)