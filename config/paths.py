# File: config/paths.py

# ============================
# Config: YAML Input Files
# ============================

PATH_CONFIG_BASE = "config"

# --- Prompt Configuration (YAML)
PATH_CONFIG_PROMPT = f"{PATH_CONFIG_BASE}/prompts.yaml"

# --- Folder where per-LLM configs are found (must match ModelKey)
# NOTE: Legacy per-model YAMLs. kept during migration; remove after MC1.1 cutover.
PATH_EVALUATED_LLM_CONFIGS = "benchmark_llms/deprecated/evaluated_llms/evaluated_llm_configs"  # DEPRECATE_AFTER_MC1_1

# --- models.yaml (evaluated LLMs catalog + global model defaults)
PATH_CONFIG_MODELS_YAML = f"{PATH_CONFIG_BASE}/models.yaml"

# --- Providers config (new layout)
#     - providers.yaml holds provider_defaults (global + per-provider)
#     - implementations/{PROVIDER}.yaml holds each provider’s runtime config
PATH_CONFIG_PROVIDERS_BASE = f"{PATH_CONFIG_BASE}/providers"
PATH_CONFIG_PROVIDERS_YAML = f"{PATH_CONFIG_PROVIDERS_BASE}/providers.yaml"
PATH_CONFIG_PROVIDERS_IMPLEMENTATIONS = f"{PATH_CONFIG_PROVIDERS_BASE}/implementations"


# ============================
# Implementation: Python Model Classes
# ============================

# --- Folder containing all final evaluated LLM implementation classes (legacy MC0)
# NOTE: Legacy folder-scan implementations. Kept only to validate parity during MC1 bring‑up.
#       Marked for removal once models.yaml + provider factory fully replace MC0 (target: MC1.1).
PATH_BENCHMARK_EVALUATED_LLM_IMPLEMENTATIONS = (
    "benchmark_llms/deprecated/evaluated_llms/implementations"  # DEPRECATE_AFTER_MC1_1
)

PATH_PROVIDERS_IMPLEMENTATIONS_CODE = "benchmark_llms/providers/implementations"


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