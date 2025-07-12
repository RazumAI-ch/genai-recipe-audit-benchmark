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
backup-db:
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb > db/backup.sql

# Restore database from previously exported SQL file
import-db:
	docker cp db/backup.sql genai-recipe-audit-benchmark-db-1:/tmp/
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < /tmp/backup.sql

# ============================================
# 📛 .PHONY: Explicitly mark all targets as non-file-based
# ============================================
#
# Why this is important:
# -----------------------
# In Make, a target is normally associated with a file. For example:
#     output.txt: input.txt
#         <build command>
#
# If a file named `output.txt` already exists and is up to date, Make skips the rule.
#
# But in this project, none of our targets (like `run`, `reset-db`, `clean`) are files.
# They're just named procedures (e.g., scripts, docker commands).
#
# If we *don't* declare them as `.PHONY`:
# - Make might skip a target if a file with the same name exists
# - Editors (like VS Code or PyCharm) might not recognize them correctly
#
# Declaring them as `.PHONY` ensures:
# - They always run when you call them
# - Make won't be confused by same-named files in your directory
# - IDEs color them properly and provide autocomplete
.PHONY: start-db stop-db clean recreate-db \
        setup-db load-llms load-deviation-types reset-db \
        run show-llms show-deviation-types show-deviations show-db-stats \
        backup-db import-db

# ============================================================================
# ⚙️ One-time test seed for validating benchmark pipeline
# - Inserts 1 benchmark_run named 'baseline-chatgpt-001'
# - Adds 100 sample_records generated as if by GPT-4o (llm_id = 1)
# - Only 2 records (2%) include deviations
# - Used to simulate LLM scoring pipeline before real integration
# ============================================================================
load-baseline-chatgpt:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/baseline_chatgpt_seed.sql