# ============================
# Benchmark LLM Configuration
# ============================

PATH_CONFIG_BENCHMARK_BASE = "config"

# Prompt configuration (used for all benchmark_llms LLMs)
PATH_CONFIG_PROMPT = f"{PATH_CONFIG_BENCHMARK_BASE}/prompts.yaml"

# Individual LLM model configs
PATH_CONFIG_OPENAI = f"{PATH_CONFIG_BENCHMARK_BASE}/evaluated_llm_configs/openai.yaml"
# PATH_CONFIG_CLAUDE = f"{PATH_CONFIG_BENCHMARK_BASE}/evaluated_llm_configs/claude.yaml"
# PATH_CONFIG_GEMINI = f"{PATH_CONFIG_BENCHMARK_BASE}/evaluated_llm_configs/gemini.yaml"


# ============================
# Log Storage Paths
# ============================

# Root log path (relative to project root)
PATH_LOGS = "archive/logs"

# Archivable logs (persisted long-term)
PATH_LOGS_ARCHIVABLE = f"{PATH_LOGS}/archivable"
PATH_LOGS_ARCHIVABLE_LLM_TRAINING = f"{PATH_LOGS_ARCHIVABLE}/llm_training"
PATH_LOGS_ARCHIVABLE_BENCHMARK_RUNS = f"{PATH_LOGS_ARCHIVABLE}/benchmark_runs"  # optional use

# Ephemeral logs (temporary run logs)
PATH_LOGS_EPHEMERAL = f"{PATH_LOGS}/ephemeral"
PATH_LOGS_DEBUG_BENCHMARK = f"{PATH_LOGS_EPHEMERAL}/debug/benchmark"
PATH_LOGS_DEBUG_TRAIN = f"{PATH_LOGS_EPHEMERAL}/debug/train"

# Unit test logs (also ephemeral)
PATH_LOGS_UNIT_TESTS = f"{PATH_LOGS_EPHEMERAL}/unit_tests"