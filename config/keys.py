# ============================
# Config Keys (used in model YAMLs)
# ============================

API_KEY_ENV = "api_key_env"      # Key to look up the env variable storing the LLM's API key
MODEL = "model"                  # Key for the LLM name or ID (e.g., 'gpt-4o')
BATCH_SIZE = "batch_size"        # Key for the number of records to send per API call
SYSTEM_PROMPT = "system_prompt"  # Key for system prompt content in prompt YAML
USER_PROMPT = "user_prompt"      # Key for user prompt content in prompt YAML

# ============================
# Global Default Values (used if model YAML omits them)
# ============================

LLM_TEMPERATURE = 0.0                # Default temperature for all completions
LLM_MAX_TOKENS_DEFAULT = 16000       # Default token cap per LLM response
LLM_DEFAULT_BATCH_SIZE = 100         # Used if a model config omits batch_size

# ============================
# Logging & Retention
# ============================

LOG_HISTORY_SIZE = 0  # How many logs to retain per model. 0 = delete all previous logs before each run.

# ============================
# Model Registry: Identifiers
# ============================

OPENAI_GPT_4O = "gpt-4o"                   # Registry key for GPT-4o model
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"     # Env var expected to hold the OpenAI key

# ============================
# Models Enabled for Benchmark
# ============================

ENABLED_BENCHMARK_MODELS = {
    OPENAI_GPT_4O,
    # CLAUDE_OPUS,
    # GEMINI_1_5_PRO,
}