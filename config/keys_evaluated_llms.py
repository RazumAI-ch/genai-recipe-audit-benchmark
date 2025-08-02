# File: config/keys_evaluated_llms.py

# ============================
# Config Keys (used in model YAMLs)
# ============================

API_KEY_ENV = "api_key_env"
MODEL = "model"
BATCH_SIZE = "batch_size"
SYSTEM_PROMPT = "system_prompt"
USER_PROMPT = "user_prompt"

# ============================
# Global Default Values
# ============================

LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS_DEFAULT = 16000
LLM_DEFAULT_BATCH_SIZE = 100

# ============================
# Logging & Retention
# ============================

LOG_HISTORY_SIZE = 0

# ============================
# Evaluated LLMs Registry: Identifiers
# ============================

OPENAI_GPT_4O = "gpt-4o"
GEMINI_1_5_PRO = "gemini-1.5-pro"
GEMINI_1_5_FLASH = "gemini-1.5-flash"
GEMINI_2_5_PRO = "gemini-2.5-pro"


# ============================
# Models Enabled for Benchmark
# ============================

ENABLED_BENCHMARK_MODELS = {
    OPENAI_GPT_4O,
    GEMINI_1_5_PRO,
}