# ============================================
# 🧪 GenAI Recipe Audit Benchmark – Makefile
# ============================================

# 🐘 PostgreSQL Container Lifecycle

start-db:
	docker-compose up -d

wait-for-db:
	@echo "Waiting for DB to become available..."
	@until docker exec genai-recipe-audit-benchmark-db-1 pg_isready -U benchmark -d benchmarkdb; do sleep 1; done

stop-db:
	docker-compose down

clean:
	docker-compose down -v

recreate-db: clean start-db wait-for-db reset-db

bootstrap-db: recreate-db show-db-stats show-schema-docs

# 🏗️ Schema + Seed Initialization

setup-db:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/schema.sql

load-llms:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/llms.sql

load-deviation-types:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/deviation_types.sql

reset-db: setup-db load-llms load-deviation-types

# ▶️ Benchmark Execution

run:
	docker-compose run --remove-orphans cli python main.py

# 🔍 Inspect DB Content

show-llms:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "SELECT id, name, provider, model FROM llms ORDER BY id;"

show-deviation-types:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "SELECT id, type, alcoa_principle, severity FROM deviation_types ORDER BY id;"

show-deviations: show-deviation-types

show-db-stats:
	docker exec -it genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT 'llms' AS table, COUNT(*) FROM llms UNION ALL \
	SELECT 'deviation_types', COUNT(*) FROM deviation_types UNION ALL \
	SELECT 'benchmark_runs', COUNT(*) FROM benchmark_runs UNION ALL \
	SELECT 'sample_records', COUNT(*) FROM sample_records UNION ALL \
	SELECT 'injected_deviations', COUNT(*) FROM injected_deviations UNION ALL \
	SELECT 'record_eval_results', COUNT(*) FROM record_eval_results UNION ALL \
	SELECT 'run_llm_results', COUNT(*) FROM run_llm_results UNION ALL \
	SELECT 'training_examples', COUNT(*) FROM training_examples UNION ALL \
	SELECT 'training_example_deviations', COUNT(*) FROM training_example_deviations;"

show-schema-docs:
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ llms'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ deviation_types'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ benchmark_runs'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ sample_records'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ injected_deviations'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ record_eval_results'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ run_llm_results'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ training_examples'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ training_example_deviations'
	docker exec -it genai-recipe-audit-benchmark-db-1 psql -U benchmark -d benchmarkdb -c '\d+ schema_docs'

# 💾 Backup / Restore Utilities

backup-db:
	docker exec genai-recipe-audit-benchmark-db-1 \
	pg_dump -U benchmark -d benchmarkdb > db/backup.sql

import-db:
	docker cp db/backup.sql genai-recipe-audit-benchmark-db-1:/tmp/
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < /tmp/backup.sql

# ============================================================================
# ⚙️ One-time test seed for validating benchmark pipeline
# ============================================================================
load-baseline-chatgpt:
	docker exec -i genai-recipe-audit-benchmark-db-1 \
	psql -U benchmark -d benchmarkdb < db/seeds/baseline_chatgpt_seed.sql

# 🤖 Training Data Generation

generate-training-examples:
	docker compose exec cli python scripts/generate_training_examples.py

check-training-data: check-training-examples check-training-example-deviations

check-training-examples:
	docker compose exec db \
	psql -U benchmark -d benchmarkdb -c "SELECT id, input_format, input_content FROM training_examples ORDER BY id DESC LIMIT 10;"

check-training-example-deviations:
	docker compose exec db \
	psql -U benchmark -d benchmarkdb -c "\
	SELECT training_example_id, deviation_type_id, source_field, explanation \
	FROM training_example_deviations \
	ORDER BY training_example_id DESC LIMIT 20;"

# ============================================
# 📛 .PHONY: Explicitly mark all targets as non-file-based
# ============================================
.PHONY: start-db wait-for-db stop-db clean recreate-db bootstrap-db \
        setup-db load-llms load-deviation-types reset-db \
        run show-llms show-deviation-types show-deviations show-db-stats show-schema-docs \
        backup-db import-db \
        load-baseline-chatgpt generate-training-examples \
        check-training-examples check-training-example-deviations