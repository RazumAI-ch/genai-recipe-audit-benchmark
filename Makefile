# ============================================
# GenAI Recipe Audit Benchmark – Makefile
# ============================================

SCHEMA_VERSION = v1.5

include .env
export

# --- MODIFIED SECTION ---
# This logic allows running `make run 10` instead of `make run NUM=10`.
# It grabs all command-line arguments after the target name (e.g., 'run').
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# If a number is passed (e.g., '10'), use it. Otherwise, default to 1.
NUM := $(or $(ARGS),1)
# --- END MODIFIED SECTION ---

DC = docker compose

# ============================================
# Benchmark Execution
# ============================================

run: _clear _ensure-db-running _fix-sequences _backup-project
	@echo "Running benchmark with NUM=$(NUM) records..."
	$(DC) run --rm cli python main.py $(NUM)
	@echo "Run finished; see archive/logs for details."

test: _ensure-db-running
	@echo "Running unit tests..."
	$(MAKE) _run-unit-tests

# ============================================
# Deployment
# ============================================

deploy-remote: _install-docker
	@echo "Deploying stack (cli + db)..."
	$(DC) pull || true
	$(DC) up -d --remove-orphans
	@$(MAKE) _wait-for-db
	@echo "DB is ready. Checking for archived DB to restore..."
	@if [ -f archive/db-latest.sql.gz ]; then \
		echo "Restoring DB from archive/db-latest.sql.gz"; \
		$(MAKE) _import-from-archive; \
		$(MAKE) _fix-sequences; \
		$(MAKE) _refresh-schema-docs; \
		$(MAKE) _show-db-stats; \
	else \
		echo "No archive/db-latest.sql.gz found. Using fresh DB."; \
	fi
	@echo "Deploy complete. You can now run: make run"

cold-redeploy: _clear _cold-redeploy
	@echo "Cold redeploy complete. You can now run: make run"

# ============================================
# Internal: DB & Docker Lifecycle
# ============================================

_ensure-db-running:
	@if docker ps -a --format '{{.Names}}' | grep -q genai-recipe-audit-benchmark-db-1; then \
		if [ "$$($(DC) ps --status=running db --format '{{.Name}}' | wc -l)" -gt 0 ]; then \
			echo "DB container running (check complete)"; \
		else \
			echo "Starting existing DB container..."; \
			$(DC) up -d db; \
			$(MAKE) _wait-for-db; \
		fi; \
	else \
		echo "No DB container found. Running full deploy-remote to restore DB..."; \
		$(MAKE) deploy-remote; \
	fi

_wait-for-db:
	@echo "Waiting for PostgreSQL in container 'db' to become ready..."
	@until $(DC) exec db pg_isready -U $(POSTGRES_USER) -d $(POSTGRES_DB) > /dev/null 2>&1; do \
		echo "  Still waiting for DB..."; \
		sleep 1; \
	done
	@echo "Database is ready!"

_docker-hard-reset:
	@echo "Hard resetting Docker: removing containers, volumes, and unused data..."
	@$(DC) down -v || true
	@docker system prune -af --volumes || true

_cold-redeploy: _docker-hard-reset _install-docker
	$(DC) pull || true
	$(DC) up -d --remove-orphans
	@$(MAKE) _wait-for-db

# ============================================
# Backup / Restore
# ============================================

backup-db: _clear _backup-project _archive-latest-logs \
           _announce-recreate-empty-db _recreate_empty_db \
           _import-from-archive _fix-sequences \
           _refresh-schema-docs _run-unit-tests _save-to-backup-file \
           _copy-latest-db-to-archive _show-db-stats

backup-db-cold: _clear
	@echo "Running standard backup-db flow..."
	@$(MAKE) backup-db
	@echo "Wiping containers/volumes and pruning Docker to simulate fresh install..."
	@$(MAKE) _docker-hard-reset
	@echo "Re-deploying stack..."
	@$(MAKE) deploy-remote
	@echo "Cold backup/restore validation finished. Run 'make run' when ready."

_announce-recreate-empty-db:
	@echo "Resetting DB and restoring schema... (this can take ~20s)..."

_recreate_empty_db:
	@$(DC) down -v > /dev/null 2>&1 || true
	@$(DC) up -d --remove-orphans > /dev/null
	@$(MAKE) _wait-for-db

_save-to-backup-file: _wait-for-db
	@mkdir -p archive/backup/db_backup
	@TIMESTAMP=$$(date "+%Y-%m-%d_%H-%M") && \
	FILE="archive/backup/db_backup/$${TIMESTAMP}_benchmarkdb_$(SCHEMA_VERSION).sql.gz" && \
	$(DC) exec db \
	pg_dump -U $(POSTGRES_USER) -d $(POSTGRES_DB) | gzip > "$$FILE" && \
	ls -1t archive/backup/db_backup/*.sql.gz | tail -n +21 | xargs rm -f --

_copy-latest-db-to-archive:
	@mkdir -p archive
	@LATEST=$$(ls -t archive/backup/db_backup/*.sql.gz | head -n 1) && \
	cp "$$LATEST" archive/db-latest.sql.gz

_import-from-archive:
	@FILE="archive/db-latest.sql.gz"; \
	USER="$(POSTGRES_USER)"; \
	DB="$(POSTGRES_DB)"; \
	if [ -f "$$FILE" ]; then \
		echo "Importing $$FILE into $$DB..."; \
		gunzip -c "$$FILE" | $(DC) exec -i db \
		psql -q -U "$$USER" -d "$$DB" > /dev/null; \
	else \
		echo "No $$FILE found. Skipping import."; \
	fi

import-db-adhoc: _clear _backup-project
	@echo "Resetting DB before importing ad-hoc backup..."
	@$(MAKE) _recreate_empty_db
	@gunzip -c "$(FILE)" | $(DC) exec -i db \
	psql -q -U $(POSTGRES_USER) -d $(POSTGRES_DB) > /dev/null
	@$(MAKE) _fix-sequences
	@$(MAKE) _refresh-schema-docs
	@$(MAKE) _show-db-stats

# ============================================
# Schema Docs & Maintenance
# ============================================

_refresh-schema-docs:
	@echo "Refreshing schema_docs..."
	@$(DC) exec db \
	pg_dump -U $(POSTGRES_USER) -d $(POSTGRES_DB) --schema-only --clean > db/schema.sql
	@$(DC) run --rm -e PGPASSWORD=$(POSTGRES_PASSWORD) cli \
	psql -U $(POSTGRES_USER) -h db -d $(POSTGRES_DB) --pset pager=off \
		-f db/makefile_db_scripts/refresh_schema_docs.sql > /dev/null
	@$(MAKE) _sort-schema-docs
	@COUNT=$$($(DC) exec -T db \
	psql -t -U $(POSTGGRES_USER) -d $(POSTGRES_DB) \
		-c "SELECT COUNT(*) FROM schema_docs WHERE description LIKE '[TODO:%]'" | tr -d '[:space:]'); \
	if [ "$$COUNT" -gt 0 ]; then \
		echo ""; \
		echo "The following fields are missing descriptions in schema_docs:"; \
		$(DC) exec db \
		psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\
			SELECT table_name, column_name FROM schema_docs \
			WHERE description LIKE '[TODO:%]' ORDER BY table_name, column_name;"; \
	fi

_fix-sequences:
	$(DC) exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -f /app/db/makefile_db_scripts/fix_all_sequences.sql

_sort-schema-docs:
	$(DC) exec db psql -q -U $(POSTGRES_USER) -d $(POSTGRES_DB) -f /app/db/makefile_db_scripts/sort_schema_docs.sql > /dev/null

_show-db-stats:
	$(DC) exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\
	SELECT relname AS table, n_live_tup AS estimated_rows \
	FROM pg_stat_user_tables ORDER BY relname;"

# ============================================
# Project Archiving
# ============================================

_archive-latest-logs:
	@BASE="archive/backup/logs_backup"; \
	mkdir -p "$$BASE"; \
	OUT_FILE="$$BASE/latest_logs.zip"; \
	mkdir -p archive/logs/archivable; \
	echo "Creating logs archive: $$OUT_FILE"; \
	cd archive/logs && zip -r "$$PWD/../backup/logs_backup/latest_logs.zip" archivable > /dev/null 2>&1

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

train-lora-tinyllama: _ensure-db-running
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
# Unit Testing
# ============================================

_run-unit-tests:
	$(DC) run --rm cli python -m unit_tests.runner_unit_tests

# ============================================
# Utils
# ============================================

_clear:
	@printf "\033c"

_install-docker:
	chmod +x scripts/install_docker.sh
	@scripts/install_docker.sh

%:
	@:

.PHONY: run test deploy-remote cold-redeploy backup-db backup-db-cold \
        _ensure-db-running _wait-for-db _docker-hard-reset _cold-redeploy \
        _import-from-archive _save-to-backup-file _copy-latest-db-to-archive \
        _refresh-schema-docs _sort-schema-docs _fix-sequences _show-db-stats \
        _archive-latest-logs _run-unit-tests _backup-project _clear _install-docker \
        import-db-adhoc docker-stats train-lora-tinyllama tail-lora-log track-lora-progress
