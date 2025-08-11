# ============================
# Config: YAML Input Files
# ============================

PATH_CONFIG_BASE = "config"

# --- Prompt Configuration (YAML)
PATH_CONFIG_PROMPT = f"{PATH_CONFIG_BASE}/prompts.yaml"

# --- Folder where per-LLM configs are found (must match ModelKey)
PATH_EVALUATED_LLM_CONFIGS = f"{PATH_CONFIG_BASE}/evaluated_llm_configs"


# ============================
# Implementation: Python Model Classes
# ============================

# --- Folder containing all final evaluated LLM implementation classes
PATH_BENCHMARK_EVALUATED_LLM_IMPLEMENTATIONS = "benchmark_llms/evaluated_llms/implementations"

PATH_CONFIG_MODELS_YAML=f"{PATH_CONFIG_BASE}/models.yaml"


# --- Folder containing per-provider configs (must match provider name in models.yaml)
PATH_PROVIDERS_CONFIGS = f"{PATH_CONFIG_BASE}/providers"


# ============================
# Output: Logging and Artifacts
# ============================

# --- Root Log Folder
PATH_LOGS = "archive/logs"

# --- Long-Term Archive Logs
PATH_LOGS_ARCHIVABLE = f"{PATH_LOGS}/archivable"
PATH_LOGS_ARCHIVABLE_LLM_TRAINING = f"{PATH_LOGS_ARCHIVABLE}/llm_training"
PATH_LOGS_ARCHIVABLE_BENCHMARK_RUNS = f"{PATH_LOGS_ARCHIVABLE}/benchmark_runs"

# --- Temporary Logs (non-archivable)
PATH_LOGS_EPHEMERAL = f"{PATH_LOGS}/ephemeral"
PATH_LOGS_DEBUG_BENCHMARK = f"{PATH_LOGS_EPHEMERAL}/debug/benchmark"
PATH_LOGS_DEBUG_TRAIN = f"{PATH_LOGS_EPHEMERAL}/debug/train"

# --- Unit Test Logs
PATH_LOGS_UNIT_TESTS = f"{PATH_LOGS_EPHEMERAL}/unit_tests"