# File: config/paths.py

# ============================
# Benchmark LLM Configuration Paths
# ============================

PATH_CONFIG_BASE = "config"

# --- Prompt Configuration (YAML)
PATH_CONFIG_PROMPT = f"{PATH_CONFIG_BASE}/prompts.yaml"

# --- Model Configuration Files (YAML per LLM)
PATH_CONFIG_EVALUATED_LLM_OPENAI_GPT_4o = f"{PATH_CONFIG_BASE}/evaluated_llm_configs/openai_gpt_4o.yaml"
PATH_CONFIG_EVALUATED_LLM_GEMINI_1_5_PRO = f"{PATH_CONFIG_BASE}/evaluated_llm_configs/gemini_1_5_pro.yaml"
PATH_CONFIG_EVALUATED_LLM_GEMINI_1_5_FLASH = f"{PATH_CONFIG_BASE}/evaluated_llm_configs/gemini_1_5_flash.yaml"

# --- Python Class Implementations (LLM code)
PATH_BENCHMARK_EVALUATED_LLM_IMPLEMENTATIONS = "benchmark_llms/evaluated_llms/implementations"


# ============================
# Benchmark Logging Paths
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