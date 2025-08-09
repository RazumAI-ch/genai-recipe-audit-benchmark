# File: Makefile
# ============================================
# GenAI Recipe Audit Benchmark – Makefile
# ============================================

# Schema Versioning
SCHEMA_VERSION = v1.5

# Ensuring .env variables are available in makefile
include .env
export

# ============================================
# Benchmark Execution
# ============================================

NUM=$(word 2,$(MAKECMDGOALS))

run: _clear _backup-project _run-unit-tests
	docker-compose run --remove-orphans cli python main.py $(NUM)

# ============================================
# SQL Utilities
# ============================================

psql: _backup-project
	docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# ============================================
# PostgreSQL Container Lifecycle
# ============================================

backup-db: _clear _backup-project _archive-latest-logs _run-unit-tests _refresh-schema-docs _save-to-backup-file _copy-latest-db-to-archive
	@echo "Resetting DB and restoring schema..."
	@$(MAKE) _recreate_empty_db
	@$(MAKE) _import-from-archive
	@$(MAKE) _fix-sequences
	@$(MAKE) _show-db-stats

_wait-for-db:
# Waiting for DB to become available
	@until docker exec genai-recipe-audit-benchmark-db-1 pg_isready -U $(POSTGRES_USER) -d $(POSTGRES_DB); do sleep 1; done

_recreate_empty_db:
	@docker-compose down -v --remove-orphans > /dev/null 2>&1
	@docker-compose up -d > /dev/null
	@$(MAKE) _wait-for-db

# ============================================
# Backup / Restore Utilities
# ============================================

_save-to-backup-file: _wait-for-db
	@mkdir -p archive/backup/db_backup
	@TIMESTAMP=$$(date "+%Y-%m-%d_%H-%M") && \
	FILE="archive/backup/db_backup/$${TIMESTAMP}_benchmarkdb_$(SCHEMA_VERSION).sql.gz" && \
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U $(POSTGRES_USER) -d $(POSTGRES_DB) | gzip > "$$FILE" && \
	ls -1t archive/backup/db_backup/*.sql.gz | tail -n +21 | xargs rm -f --

# NOTE: keep gzip extension end-to-end to avoid format confusion
_copy-latest-db-to-archive:
	@mkdir -p archive
	@LATEST=$$(ls -t archive/backup/db_backup/*.sql.gz | head -n 1) && \
	cp "$$LATEST" archive/db-latest.sql.gz

_import-from-archive:
	@FILE="archive/db-latest.sql.gz"; \
	USER="$(POSTGRES_USER)"; \
	DB="$(POSTGRES_DB)"; \
	gunzip -c "$$FILE" | docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -q -U "$$USER" -d "$$DB" > /dev/null

# Import any .gz backup by specifying FILE=...
# Example: make import-db-adhoc FILE=archive/backup/db_backup/2025-07-26_19-46.sql.gz
import-db-adhoc: _clear _backup-project
	@echo "Resetting DB before importing ad-hoc backup..."
	@$(MAKE) _recreate_empty_db
	@gunzip -c "$(FILE)" | docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -q -U $(POSTGRES_USER) -d $(POSTGRES_DB) > /dev/null
	@$(MAKE) _fix-sequences
	@$(MAKE) _refresh-schema-docs
	@$(MAKE) _show-db-stats

_refresh-schema-docs:
	@docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U $(POSTGRES_USER) -d $(POSTGRES_DB) --schema-only --clean > db/schema.sql

	@docker compose run --rm -e PGPASSWORD=$(POSTGRES_PASSWORD) cli \
	psql -U $(POSTGRES_USER) -h db -d $(POSTGRES_DB) --pset pager=off -f db/makefile_db_scripts/refresh_schema_docs.sql > /dev/null

	@$(MAKE) _sort-schema-docs

	@COUNT=$$(docker compose exec -T db \
	psql -t -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "SELECT COUNT(*) FROM schema_docs WHERE description LIKE '[TODO:%]'" | tr -d '[:space:]'); \
	if [ "$$COUNT" -gt 0 ]; then \
	echo ""; \
	echo "The following fields are missing descriptions in schema_docs:"; \
	echo "Please generate and insert descriptions manually via SQL."; \
	docker compose exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\
	SELECT table_name, column_name FROM schema_docs \
	WHERE description LIKE '[TODO:%]' ORDER BY table_name, column_name;"; \
	fi

# Fix all PostgreSQL sequences to match current data state
_fix-sequences:
	docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -f /app/db/makefile_db_scripts/fix_all_sequences.sql

_sort-schema-docs:
	docker compose exec db psql -q -U $(POSTGRES_USER) -d $(POSTGRES_DB) -f /app/db/makefile_db_scripts/sort_schema_docs.sql > /dev/null

_show-db-stats:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\
	SELECT relname AS table, n_live_tup AS estimated_rows \
	FROM pg_stat_user_tables ORDER BY relname;"

# ============================================
# Archiving of DB and logs
# ============================================

_archive-latest-logs:
	@BASE="archive/backup/logs_backup"; \
	mkdir -p "$$BASE"; \
	OUT_FILE="$$BASE/latest_logs.zip"; \
	mkdir -p archive/logs/archivable; \
	echo "Creating logs archive: $$OUT_FILE"; \
	cd archive/logs && zip -r "$$PWD/../backup/logs_backup/latest_logs.zip" archivable > /dev/null 2>&1

# ============================================
# Project Code & Config Archive
# ============================================

_backup-project:
	@BASE="archive/backup/project_code_and_config_backup"; \
	mkdir -p "$$BASE"; \
	OUT_FILE="$$BASE/latest_project_code_and_config.zip"; \
	FOLDERS="benchmark_llms config db docs loggers train_llms unit_tests"; \
	INCLUDE=""; \
	for d in $$FOLDERS; do \
	  if [ -d "$$d" ]; then INCLUDE="$$INCLUDE $$d"; fi; \
	done; \
	ROOT_FILES=$$(find . -maxdepth 1 -type f -not -name "*.zip"); \
	echo "Creating project archive: $$OUT_FILE"; \
	zip -r "$$OUT_FILE" $$INCLUDE $$ROOT_FILES > /dev/null

# ============================================
# Training
# ============================================

docker-stats:
	docker stats

train-lora-tinyllama: _wait-for-db
	docker run -it --rm \
	  --name lora-trainer \
	  --memory=117g \
	  --network genai-recipe-audit-benchmark_default \
	  -v $(PWD):/app \
	  -v ~/.cache/huggingface:/root/.cache/huggingface \
	  -w /app \
	  genai-recipe-audit-benchmark-cli \
	  python training/train_lora/TinyLlamaLoRATrainer.py

tail-lora-log:
	@while [ ! -f archive/logs/training/lora/latest.log ]; do sleep 1; done
	@tail -f archive/logs/training/lora/latest.log

track-lora-progress:
	python3 training/utils/track_lora_progress.py

# ============================================
# Training Data Generation
# ============================================

generate-training-examples:
	docker compose exec cli python training/generate_training_examples.py

check-training-data: check-training-examples check-training-example-deviations check-training-llm-sources

check-training-examples:
	docker compose exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "SELECT id, input_format, input_content FROM training_examples ORDER BY id DESC LIMIT 10;"

check-training-example-deviations:
	docker compose exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\
	SELECT training_example_id, deviation_type_id, source_field, explanation \
	FROM training_example_deviations \
	ORDER BY training_example_id DESC LIMIT 20;"

check-training-llm-sources:
	docker compose exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\
	SELECT id, source_llm FROM training_examples ORDER BY id DESC LIMIT 10;"

# ============================================
# Unit Testing
# ============================================

_run-unit-tests:
	docker-compose run --rm --remove-orphans cli python -m unit_tests.runner_unit_tests

# ============================================
# Utils
# ============================================

_clear:
	@printf "\033c"

%:
	@:

# ============================================
# PHONY Targets
# ============================================

.PHONY: run psql backup-db docker-stats train-lora-tinyllama tail-lora-log \
        track-lora-progress generate-training-examples check-training-data \
        check-training-examples check-training-example-deviations \
        check-training-llm-sources import-db-adhoc _clear \
        _wait-for-db _recreate_empty_db _save-to-backup-file _import-from-archive \
        _refresh-schema-docs _sort-schema-docs _fix-sequences _show-db-stats \
        _archive-latest-logs _run-unit-tests _backup-project