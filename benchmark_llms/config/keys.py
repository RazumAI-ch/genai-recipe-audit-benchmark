# File: config/keys.py

# ============================
# General Config Keys
# ============================
API_KEY_ENV = "api_key_env"
MODEL = "model"
BATCH_SIZE = "batch_size"
SYSTEM_PROMPT = "system_prompt"
USER_PROMPT = "user_prompt"

LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS_DEFAULT = 16000  # or whatever your intended default is

# ============================
# OpenAI Model(s)
# ============================
OPENAI_GPT_4O = "gpt-4o"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


# ============================
# Enabled Benchmark Models
# ============================

ENABLED_BENCHMARK_MODELS = {
    OPENAI_GPT_4O,
    # CLAUDE_OPUS,
    # GEMINI_1_5_PRO,
}