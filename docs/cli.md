# 🧰 Command-Line Interface (CLI) Guide – GenAI Recipe Audit Benchmark

This guide documents how to interact with the project via the command line, including:
- Starting/stopping the PostgreSQL container
- Resetting the database schema
- Loading LLM and deviation seeds
- Viewing table contents and database stats
- Running the benchmark

---

## 📦 Prerequisites

- Docker installed and available in your terminal
- `make` installed (comes preinstalled on macOS and Linux)
- Project cloned locally

---

## 🗂️ Project Commands via `make`

The project includes a `Makefile` with helpful shortcuts:

| Command                      | Description                                                   |
|------------------------------|---------------------------------------------------------------|
| `make start-db`              | Start PostgreSQL container                                    |
| `make wait-for-db`           | Wait for DB container to be ready before executing commands   |
| `make stop-db`               | Stop the PostgreSQL container                                 |
| `make clean`                 | Stop and remove container and volume                          |
| `make recreate-db`           | Full reset: wipe DB, recreate schema, load all seeds          |
| `make setup-db`              | Drop and recreate schema from `db/schema.sql`                 |
| `make load-llms`             | Insert LLMs into `llms` table from `db/seeds/llms.sql`        |
| `make load-deviation-types`  | Insert ALCOA+ deviation types into `deviation_types` table    |
| `make reset-db`              | Run both schema reset and all seed inserts                    |
| `make show-llms`             | Show current contents of the `llms` table                     |
| `make show-deviation-types`  | Show current contents of the `deviation_types` table          |
| `make show-deviations`       | Alias for `make show-deviation-types`                         |
| `make show-db-stats`         | Overview of row counts in all key benchmark tables            |
| `make show-table-definitions`| Show full schema definition of all tables                     |
| `make run`                   | Execute the benchmark (`main.py`)                             |
| `make bootstrap-db`          | Full bootstrap: reset schema, seed LLMs/deviations, insert 100 samples, show table stats + definitions |

Run these from your project root, for example:

```bash
make bootstrap-db
make run
```

---

## 🛠️ Manual Commands (If Needed)

### ▶️ Load the Schema (alternative to `make setup-db`)
```bash
docker exec -i genai-recipe-audit-benchmark-db-1 \
  psql -U benchmark -d benchmarkdb < db/schema.sql
```

### ▶️ Load LLMs (alternative to `make load-llms`)
```bash
docker exec -i genai-recipe-audit-benchmark-db-1 \
  psql -U benchmark -d benchmarkdb < db/seeds/2025-07-15_llms.sql
```

### ▶️ Load Deviation Types (alternative to `make load-deviation-types`)
```bash
docker exec -i genai-recipe-audit-benchmark-db-1 \
  psql -U benchmark -d benchmarkdb < db/seeds/2025-07-15_deviation_types.sql
```

### 🧪 Query a Table (e.g., LLMs)
```bash
docker exec -it genai-recipe-audit-benchmark-db-1 \
  psql -U benchmark -d benchmarkdb -c 'SELECT * FROM llms;'
```

### 📊 Run Table Stats Query (manual equivalent of `make show-db-stats`)
```bash
docker exec -it genai-recipe-audit-benchmark-db-1 \
  psql -U benchmark -d benchmarkdb -c "\
  SELECT 'llms' AS table, COUNT(*) FROM llms UNION ALL \
  SELECT 'deviation_types', COUNT(*) FROM deviation_types UNION ALL \
  SELECT 'benchmark_runs', COUNT(*) FROM benchmark_runs UNION ALL \
  SELECT 'sample_records', COUNT(*) FROM sample_records UNION ALL \
  SELECT 'injected_deviations', COUNT(*) FROM injected_deviations UNION ALL \
  SELECT 'record_eval_results', COUNT(*) FROM record_eval_results UNION ALL \
  SELECT 'run_llm_results', COUNT(*) FROM run_llm_results;"
```

### 🧾 View Table Definitions (manual equivalent of `make show-table-definitions`)
```bash
docker exec -it genai-recipe-audit-benchmark-db-1 \
  psql -U benchmark -d benchmarkdb -c "\d+ benchmark_runs"
docker exec -it genai-recipe-audit-benchmark-db-1 \
  psql -U benchmark -d benchmarkdb -c "\d+ sample_records"
...
```

---

## 🧪 Running the Benchmark

Once your schema and deviation types are loaded, run:

```bash
make run
```

This runs the current configuration from `main.py`. Later, you’ll be able to pass flags like:

```bash
python main.py run --llms all --samples 100
```

---

## 📄 See Also

- [`README.md`](../README.md) – project overview  
- [`db/schema.sql`](../db/schema.sql) – database structure  
- [`db/seeds/llms.sql`](../db/backups/2025-07-15_llms.sql) – seed model list  
- [`db/seeds/deviation_types.sql`](../db/backups/2025-07-15_deviation_types.sql) – ALCOA+ deviation types