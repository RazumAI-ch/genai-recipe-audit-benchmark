# File: Makefile
# ============================================
# 🧪 GenAI Recipe Audit Benchmark – Makefile
# ============================================

# 📐 Schema Versioning
SCHEMA_VERSION ?= v1.4


# ▶️ Benchmark Execution

run:
	docker-compose run --remove-orphans cli python main.py

# Starting SQL
psql:
	docker compose exec db psql -U benchmark -d benchmarkdb

# 🐘 PostgreSQL Container Lifecycle

backup-db: refresh-schema-docs save_to_file copy-latest-db-to-archive archive-latest-logs
	@echo "♻️  Resetting DB and restoring schema..."
	@$(MAKE) recreate_empty_db
	@$(MAKE) import-db
	@echo "✅ Backup, reset, and import completed."
	@$(MAKE) show-stats

wait-for-db:
	@echo "Waiting for DB to become available..."
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
	echo "📦 Saving backup: $${FILE}" && \
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb | gzip > "$$FILE" && \
	echo "✅ Backup saved." && \
	ls -1t db/backups/*.sql.gz | tail -n +21 | xargs rm -f --

import-db:
	@FILE=$$(ls -t db/backups/*.sql.gz | head -n 1); \
	echo "📥 Importing backup into benchmarkdb from $$FILE" && \
	gunzip -c "$$FILE" | docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -q -U benchmark -d benchmarkdb > /dev/null

show-stats:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT relname AS table, n_live_tup AS estimated_rows \
	FROM pg_stat_user_tables ORDER BY relname;"


refresh-schema-docs:
	@echo "📚 Updating db/schema.sql based on actual DB schema"
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb --schema-only --clean > db/schema.sql
	@echo "📚 Updating schema_docs with any missing fields..."
	docker compose run --rm -e PGPASSWORD=benchmark cli \
	psql -U benchmark -h db -d benchmarkdb -f db/refresh_schema_docs.sql
	@echo "✅ Schema and docs are now in sync."

# Archiving of db and logs

# Copy latest DB backup into archive/ with static filename
copy-latest-db-to-archive:
	@echo "📦 Copying latest DB backup to archive/db-backup-latest.zip"
	@mkdir -p archive
	@LATEST=$$(ls -t db/backups/*.sql.gz | head -n 1) && \
	cp "$$LATEST" archive/db-backup-latest.zip && \
	echo "✅ Copied: $$LATEST → archive/db-backup-latest.zip"

archive-latest-logs:
	@echo "📦 Archiving latest logs to archive/logs-latest.zip"
	@mkdir -p archive
	@zip -j archive/logs-latest.zip logs/training/lora/* || echo "No logs to archive"
	@echo "✅ Logs archived to archive/logs-latest.zip"


# Training

docker-stats:
	docker stats

train-lora-tinyllama: wait-for-db
	docker run -it --rm \
	  --memory=117g \
	  --network genai-recipe-audit-benchmark_default \
	  -v $(PWD):/app \
	  -v ~/.cache/huggingface:/root/.cache/huggingface \
	  -w /app \
	  genai-recipe-audit-benchmark-cli \
	  python scripts/train_lora/TinyLlamaLoRATrainer.py

tail-lora-log:
	@echo "⏳ Waiting for logs/training/lora/latest.log to appear..."
	@while [ ! -f logs/training/lora/latest.log ]; do sleep 1; done
	@echo "📄 Log found — now tailing:"
	@echo
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

# ============================================
# 📛 .PHONY: Explicitly mark all targets as non-file-based
# ============================================

.PHONY: wait-for-db recreate_empty_db backup-db archive-latest-logs \
        setup-db run show-db-stats \
        save_to_file import-db restore-into-new-db generate-training-examples \
        check-training-examples check-training-example-deviations check-training-llm-sources