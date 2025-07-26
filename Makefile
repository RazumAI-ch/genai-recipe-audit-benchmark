# File: Makefile
# ============================================
# 🧪 GenAI Recipe Audit Benchmark – Makefile
# ============================================

# 📐 Schema Versioning
SCHEMA_VERSION ?= v1.4

# ▶️ Benchmark Execution

run: clear
	@echo "make run"
	docker-compose run --remove-orphans cli python main.py

show-db-samples-stats:
	docker compose exec db psql -U benchmark -d benchmarkdb -c "\
	SELECT '📊 Total sample_records' AS metric, COUNT(*) AS value FROM sample_records; \
	SELECT '📌 Records with deviations' AS metric, COUNT(DISTINCT sample_record_id) AS value FROM injected_deviations; \
	SELECT '🔴 Records with critical deviations' AS metric, COUNT(DISTINCT id.sample_record_id) AS value \
	FROM injected_deviations id \
	JOIN deviation_types d ON id.deviation_type_id = d.id \
	WHERE d.severity = 'critical'; \
	SELECT '🟠 Records with major deviations' AS metric, COUNT(DISTINCT id.sample_record_id) AS value \
	FROM injected_deviations id \
	JOIN deviation_types d ON id.deviation_type_id = d.id \
	WHERE d.severity = 'major'; \
	SELECT '🟢 Records with minor deviations' AS metric, COUNT(DISTINCT id.sample_record_id) AS value \
	FROM injected_deviations id \
	JOIN deviation_types d ON id.deviation_type_id = d.id \
	WHERE d.severity = 'minor';"

# Starting SQL
psql:
	docker compose exec db psql -U benchmark -d benchmarkdb

# 🐘 PostgreSQL Container Lifecycle

backup-db: clear refresh-schema-docs save_to_file copy-latest-db-to-archive archive-latest-logs
	@echo "Resetting DB and restoring schema..."
	@$(MAKE) recreate_empty_db
	@$(MAKE) import-db
	@$(MAKE) fix-sequences
	@$(MAKE) show-db-stats

wait-for-db:
#@echo "Waiting for DB to become available..."
	@until docker exec genai-recipe-audit-benchmark-db-1 pg_isready -U benchmark -d benchmarkdb; do sleep 1; done

recreate_empty_db:
	@docker-compose down -v --remove-orphans > /dev/null 2>&1
	@docker-compose up -d > /dev/null
	@$(MAKE) wait-for-db

# 💾 Backup / Restore Utilities

save_to_file: wait-for-db
	@mkdir -p db/backups
	@TIMESTAMP=$$(date "+%Y-%m-%d_%H-%M") && \
	FILE="db/backups/$${TIMESTAMP}_benchmarkdb_$(SCHEMA_VERSION).sql.gz" && \
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb | gzip > "$$FILE" && \
	ls -1t db/backups/*.sql.gz | tail -n +21 | xargs rm -f --

import-db:
	@FILE="archive/db-backup-latest.zip"; \
	gunzip -c "$$FILE" | docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -q -U benchmark -d benchmarkdb > /dev/null

# 💾 Import any .gz backup by specifying FILE=...
# Example of running: make import-db-adhoc FILE=db/backups/2025-07-26_19-46.gz
import-db-adhoc:
	@echo "Resetting DB before importing ad-hoc backup..."
	@$(MAKE) recreate_empty_db
	@gunzip -c "$(FILE)" | docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -q -U benchmark -d benchmarkdb > /dev/null
	@$(MAKE) fix-sequences
	@$(MAKE) refresh-schema-docs
	@$(MAKE) show-db-stats

refresh-schema-docs:
	@docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb --schema-only --clean > db/schema.sql

	@docker compose run --rm -e PGPASSWORD=benchmark cli \
	psql -U benchmark -h db -d benchmarkdb --pset pager=off -f db/refresh_schema_docs.sql > /dev/null

	@$(MAKE) sort-schema-docs

	@COUNT=$$(docker compose exec -T db \
	psql -t -U benchmark -d benchmarkdb -c "SELECT COUNT(*) FROM schema_docs WHERE description LIKE '[TODO:%]'" | tr -d '[:space:]'); \
	if [ "$$COUNT" -gt 0 ]; then \
	echo ""; \
	echo "🔍 The following fields are missing descriptions in schema_docs:"; \
	echo "📌 Please generate and insert descriptions manually via SQL."; \
	docker compose exec db \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT table_name, column_name FROM schema_docs \
	WHERE description LIKE '[TODO:%]' ORDER BY table_name, column_name;"; \
	fi


show-db-stats:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT relname AS table, n_live_tup AS estimated_rows \
	FROM pg_stat_user_tables ORDER BY relname;"

# 🛠 Fix all PostgreSQL sequences to match current data state
# When dropping and restoring the DB from a backup, Postgres does not automatically
# reset sequences (like sample_records_id_seq, injected_deviations_id_seq, etc.)
# to align with the current max(id) values in their respective tables.
# This target runs a script that resets all sequences to prevent primary key conflicts.
fix-sequences:
	docker compose exec db psql -U benchmark -d benchmarkdb -f /app/db/fix_all_sequences.sql

# 📑 Ensures schema_docs entries are grouped by table and sorted by column name
# This improves readability when querying schema_docs directly,
# making it easier to view or edit all fields for a specific table.
# Especially useful after adding new fields, which would otherwise appear at the end.
sort-schema-docs:
	docker compose exec db psql -q -U benchmark -d benchmarkdb -f /app/db/sort_schema_docs.sql > /dev/null

# Archiving of db and logs

copy-latest-db-to-archive:
	@mkdir -p archive
	@LATEST=$$(ls -t db/backups/*.sql.gz | head -n 1) && \
	cp "$$LATEST" archive/db-backup-latest.zip

archive-latest-logs:
	@mkdir -p archive
	@zip -j archive/logs-latest.zip logs/training/lora/* > /dev/null 2>&1 || true

# Training

docker-stats:
	docker stats

train-lora-tinyllama: wait-for-db
	docker run -it --rm \
	  --name lora-trainer \
	  --memory=117g \
	  --network genai-recipe-audit-benchmark_default \
	  -v $(PWD):/app \
	  -v ~/.cache/huggingface:/root/.cache/huggingface \
	  -w /app \
	  genai-recipe-audit-benchmark-cli \
	  python scripts/train_lora/TinyLlamaLoRATrainer.py

tail-lora-log:
	@while [ ! -f logs/training/lora/latest.log ]; do sleep 1; done
	@tail -f logs/training/lora/latest.log

track-lora-progress:
	python3 scripts/utils/track_lora_progress.py

# 🤖 Training Data Generation

generate-training-examples:
	docker compose exec cli python scripts/generate_training_examples.py

check-training-data: check-training-examples check-training-example-deviations check-training-llm-sources

check-training-examples:
	docker compose exec db \
	psql -U benchmark -d benchmarkdb -c "SELECT id, input_format, input_content FROM training_examples ORDER BY id DESC LIMIT 10;"

check-training-example-deviations:
	docker compose exec db \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT training_example_id, deviation_type_id, source_field, explanation \
	FROM training_example_deviations \
	ORDER BY training_example_id DESC LIMIT 20;"

check-training-llm-sources:
	docker compose exec db \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT id, source_llm FROM training_examples ORDER BY id DESC LIMIT 10;"

# Utils

clear:
	@printf "\033c"

# ============================================
# 📛 .PHONY: Explicitly mark all targets as non-file-based
# ============================================

.PHONY: wait-for-db recreate_empty_db backup-db archive-latest-logs \
        setup-db run show-db-stats \
        save_to_file import-db restore-into-new-db generate-training-examples \
        check-training-examples check-training-example-deviations check-training-llm-sources

# One off commands - to be removed later