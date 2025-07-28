# File: config/keys.py

# ============================
# General Config Keys
# ============================

API_KEY_ENV = "api_key_env"          # Name of env variable storing the API key for the LLM
MODEL = "model"                      # Key in model config indicating model identifier (e.g., 'gpt-4o')
BATCH_SIZE = "batch_size"            # Number of records to send per LLM call (if batching is supported)
SYSTEM_PROMPT = "system_prompt"      # Key for the system role message in prompt config
USER_PROMPT = "user_prompt"          # Key for the user role message in prompt config

LLM_TEMPERATURE = 0.0                # Default temperature used in all LLM completions
LLM_MAX_TOKENS_DEFAULT = 16000       # Default maximum tokens allowed in a single LLM response
LLM_DEFAULT_BATCH_SIZE = 50          # Used if model-specific config omits batch_size

# Log retention policy — number of recent log files to retain per model.
# Set to 0 to delete all logs before each new run (minimal storage mode).
# Recommended: Set to 5–10 in long-running benchmarks to retain history.
LOG_HISTORY_SIZE = 0

# ============================
# OpenAI Model(s)
# ============================

OPENAI_GPT_4O = "gpt-4o"                   # Registry key for GPT-4o model
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"     # Env variable expected to hold OpenAI API key

# ============================
# Enabled Benchmark Models
# ============================

ENABLED_BENCHMARK_MODELS = {
    OPENAI_GPT_4O,
    # CLAUDE_OPUS,
    # GEMINI_1_5_PRO,
}