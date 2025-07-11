# ============================================
# 🧪 GenAI Recipe Audit Benchmark – Makefile
# ============================================

# Start PostgreSQL container
start-db:
	docker-compose up -d

# Stop all containers
stop-db:
	docker-compose down

# Clean up containers and volumes (erases DB!)
clean:
	docker-compose down -v

# Drop everything and start fresh
recreate-db: clean start-db reset-db

# Load schema (drops + recreates all tables, no seeds)
setup-db:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/schema.sql

# Load LLM definitions
load-llms:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/llms.sql

# Load ALCOA+ deviation types
load-deviation-types:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/deviation_types.sql

# Full reset and seed
reset-db: setup-db load-llms load-deviation-types

# Run the benchmark
run:
	python main.py

# View contents of LLMs table
show-llms:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "SELECT id, name, provider, model FROM llms ORDER BY id;"

# View contents of Deviation Types table
show-deviation-types:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "SELECT id, type, alcoa_principle, severity FROM deviation_types ORDER BY id;"


# Show DB record counts across key tables
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