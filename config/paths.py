# File: config/paths.py

# Prompt configuration
PATH_CONFIG_PROMPT = "config/prompts.yaml"

# Base logs path
PATH_LOGS = "logs"

# Archivable logs (long-term storage)
PATH_LOGS_ARCHIVABLE = f"{PATH_LOGS}/archivable"
PATH_LOGS_ARCHIVABLE_LLM_TRAINING = f"{PATH_LOGS_ARCHIVABLE}/llm_training"
PATH_LOGS_ARCHIVABLE_BENCHMARK_RUNS = f"{PATH_LOGS_ARCHIVABLE}/benchmark_runs"  # if needed later

# Ephemeral logs (temporary, discardable)
PATH_LOGS_EPHEMERAL = f"{PATH_LOGS}/ephemeral"
PATH_LOGS_DEBUG = f"{PATH_LOGS_EPHEMERAL}/debug"

# Unit test logs (ephemeral by design)
PATH_LOGS_UNIT_TESTS = f"{PATH_LOGS_EPHEMERAL}/unit_tests_logs"
PATH_LOGS_UNIT_TESTS_BENCHMARK = f"{PATH_LOGS_UNIT_TESTS}/benchmark_unit_tests_logs"
PATH_LOGS_UNIT_TESTS_TRAINING = f"{PATH_LOGS_UNIT_TESTS}/training_unit_tests_logs"

# LLM model configurations
PATH_CONFIG_OPENAI = "config/openai.yaml"