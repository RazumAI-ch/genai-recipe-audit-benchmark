# ============================================
# 🧪 GenAI Recipe Audit Benchmark – Makefile
# ============================================

# 🐘 PostgreSQL Container Lifecycle

# Start PostgreSQL container in detached mode
start-db:
	docker-compose up -d

# Stop and remove containers only (data remains)
stop-db:
	docker-compose down

# Stop containers AND remove attached volumes (⚠️ this erases all DB data!)
clean:
	docker-compose down -v

# Completely reset the DB from scratch: clean + recreate + seed
recreate-db: clean start-db reset-db

# 🏗️ Schema + Seed Initialization

# Apply schema only (no seeds); drops + recreates all tables
setup-db:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/schema.sql

# Load predefined LLMs into the llms table
load-llms:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/llms.sql

# Load ALCOA+ deviation types into the deviation_types table
load-deviation-types:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/deviation_types.sql

# Run full DB setup: schema + LLMs + deviation types
reset-db: setup-db load-llms load-deviation-types

# ▶️ Benchmark Execution

# Run the benchmark script (main entry point)
run:
	python main.py

# 🔍 Inspect DB Content

# Show all registered LLMs
show-llms:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "SELECT id, name, provider, model FROM llms ORDER BY id;"

# Show all available deviation types
show-deviation-types:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "SELECT id, type, alcoa_principle, severity FROM deviation_types ORDER BY id;"

# Alias for convenience
show-deviations: show-deviation-types

# Show row counts for all major benchmark tables
show-db-stats:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT 'llms' AS table, COUNT(*) FROM llms UNION ALL \
	SELECT 'deviation_types', COUNT(*) FROM deviation_types UNION ALL \
	SELECT 'benchmark_runs', COUNT(*) FROM benchmark_runs UNION ALL \
	SELECT 'sample_records', COUNT(*) FROM sample_records UNION ALL \
	SELECT 'deviations', COUNT(*) FROM deviations UNION ALL \
	SELECT 'record_eval_results', COUNT(*) FROM record_eval_results UNION ALL \
	SELECT 'run_llm_results', COUNT(*) FROM run_llm_results;"

# 💾 Backup / Restore Utilities

# Export full database contents to SQL file (backup)
export-db:
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb > db/backup.sql

# Restore database from previously exported SQL file
import-db:
	docker cp db/backup.sql genai-recipe-audit-benchmark-db-1:/tmp/
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < /tmp/backup.sql