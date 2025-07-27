# File: Makefile
# ============================================
# GenAI Recipe Audit Benchmark – Makefile
# ============================================

# Schema Versioning
SCHEMA_VERSION ?= v1.4

# Benchmark Execution

NUM=$(word 2,$(MAKECMDGOALS))

run: _clear
	docker-compose run --remove-orphans cli python main.py $(NUM)

# Starting SQL

psql:
	docker compose exec db psql -U benchmark -d benchmarkdb

# PostgreSQL Container Lifecycle

backup-db: _clear _refresh-schema-docs _save_to_file _copy-latest-db-to-archive _archive-latest-logs
	@echo "Resetting DB and restoring schema..."
	@$(MAKE) _recreate_empty_db
	@$(MAKE) _import-db
	@$(MAKE) _fix-sequences
	@$(MAKE) _show-db-stats

_wait-for-db:
# Waiting for DB to become available
	@until docker exec genai-recipe-audit-benchmark-db-1 pg_isready -U benchmark -d benchmarkdb; do sleep 1; done

_recreate_empty_db:
	@docker-compose down -v --remove-orphans > /dev/null 2>&1
	@docker-compose up -d > /dev/null
	@$(MAKE) _wait-for-db

# Backup / Restore Utilities

_save_to_file: _wait-for-db
	@mkdir -p archive/backup/db-backup
	@TIMESTAMP=$$(date "+%Y-%m-%d_%H-%M") && \
	FILE="archive/backup/db-backup/$${TIMESTAMP}_benchmarkdb_$(SCHEMA_VERSION).sql.gz" && \
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb | gzip > "$$FILE" && \
	ls -1t archive/backup/db-backup/*.sql.gz | tail -n +21 | xargs rm -f --

_import-db:
	@FILE="archive/db-archive.zip"; \
	gunzip -c "$$FILE" | docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -q -U benchmark -d benchmarkdb > /dev/null

# Import any .gz backup by specifying FILE=...
# Example: make import-db-adhoc FILE=archive/backup/db-backup/2025-07-26_19-46.gz
import-db-adhoc: _clear
	@echo "Resetting DB before importing ad-hoc backup..."
	@$(MAKE) _recreate_empty_db
	@gunzip -c "$(FILE)" | docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -q -U benchmark -d benchmarkdb > /dev/null
	@$(MAKE) _fix-sequences
	@$(MAKE) _refresh-schema-docs
	@$(MAKE) _show-db-stats

_refresh-schema-docs:
	@docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb --schema-only --clean > db/schema.sql

	@docker compose run --rm -e PGPASSWORD=benchmark cli \
	psql -U benchmark -h db -d benchmarkdb --pset pager=off -f db/makefile_db_scripts/refresh_schema_docs.sql > /dev/null

	@$(MAKE) _sort-schema-docs

	@COUNT=$$(docker compose exec -T db \
	psql -t -U benchmark -d benchmarkdb -c "SELECT COUNT(*) FROM schema_docs WHERE description LIKE '[TODO:%]'" | tr -d '[:space:]'); \
	if [ "$$COUNT" -gt 0 ]; then \
	echo ""; \
	echo "The following fields are missing descriptions in schema_docs:"; \
	echo "Please generate and insert descriptions manually via SQL."; \
	docker compose exec db \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT table_name, column_name FROM schema_docs \
	WHERE description LIKE '[TODO:%]' ORDER BY table_name, column_name;"; \
	fi

# Fix all PostgreSQL sequences to match current data state
# When dropping and restoring the DB from a backup, Postgres does not automatically
# reset sequences (like sample_records_id_seq, injected_deviations_id_seq, etc.)
# to align with the current max(id) values in their respective tables.
# This target runs a script that resets all sequences to prevent primary key conflicts.
_fix-sequences:
	docker compose exec db psql -U benchmark -d benchmarkdb -f /app/db/makefile_db_scripts/fix_all_sequences.sql

# Ensures schema_docs entries are grouped by table and sorted by column name
# This improves readability when querying schema_docs directly,
# making it easier to view or edit all fields for a specific table.
# Especially useful after adding new fields, which would otherwise appear at the end.
_sort-schema-docs:
	docker compose exec db psql -q -U benchmark -d benchmarkdb -f /app/db/makefile_db_scripts/sort_schema_docs.sql > /dev/null

_show-db-stats:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT relname AS table, n_live_tup AS estimated_rows \
	FROM pg_stat_user_tables ORDER BY relname;"

# Archiving of db and logs

_copy-latest-db-to-archive:
	@mkdir -p archive
	@LATEST=$$(ls -t archive/backup/db-backup/*.sql.gz | head -n 1) && \
	cp "$$LATEST" archive/db-archive.zip

_archive-latest-logs:
	@mkdir -p archive
	@cd archive/logs && zip -r ../../archive/logs-archive.zip archivable > /dev/null 2>&1

# Training

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
	  python scripts/train_lora/TinyLlamaLoRATrainer.py

tail-lora-log:
	@while [ ! -f archive/logs/training/lora/latest.log ]; do sleep 1; done
	@tail -f archive/logs/training/lora/latest.log

track-lora-progress:
	python3 scripts/utils/track_lora_progress.py

# Training Data Generation

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

_clear:
	@printf "\033c"

# Catch-all rule to prevent errors on extra CLI arguments
# When using `make run none` or `make run 200`, `make` interprets each word as a separate target.
# For example:
#   make run none
# Is treated as:
#   - target `run`
#   - and target `none`
# Since `none` is not a real rule, `make` would normally throw:
#   "make: *** No rule to make target `none`.  Stop."
#
# This catch-all pattern rule matches any additional word passed to `make`
# that does not correspond to a defined target, and silently does nothing with it.
# This is safe because the actual logic for `run` is handled in main.py,
# and arguments like none, 100, or 300 are interpreted in Python—not in Make.

%:
	@:

# PHONY Targets

.PHONY: run psql backup-db docker-stats train-lora-tinyllama tail-lora-log \
        track-lora-progress generate-training-examples check-training-data \
        check-training-examples check-training-example-deviations \
        check-training-llm-sources import-db-adhoc _clear \
        _wait-for-db _recreate_empty_db _save_to_file _import-db \
        _refresh-schema-docs _sort-schema-docs _fix-sequences _show-db-stats \
        _copy-latest-db-to-archive _archive-latest-logs