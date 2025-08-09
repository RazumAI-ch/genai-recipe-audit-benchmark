# File: config/keys_evaluated_llms.py
# ============================
# Config keys and legacy identifiers (to be removed post-YAML migration)
# ============================

# ----------------------------
# Spec Version Guards
# ----------------------------
MODELS_SPEC_VERSION_MIN = "0.1.0"
REMOVE_AFTER_MODELS_SPEC = "1.0.0"  # canonical threshold for removing legacy code

# ----------------------------
# Config Keys (used in model YAMLs)
# ----------------------------
API_KEY_ENV = "api_key_env"
MODEL = "model"
BATCH_SIZE = "batch_size"
SYSTEM_PROMPT = "system_prompt"
USER_PROMPT = "user_prompt"

# ----------------------------
# Current global LLM defaults (legacy — superseded by YAML)
# ----------------------------
LLM_TEMPERATURE = 0.0                 # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use global_model_defaults.temperature
LLM_MAX_TOKENS_DEFAULT = 16000        # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use global_model_defaults.max_tokens
LLM_DEFAULT_BATCH_SIZE = 100          # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use provider_defaults.*.batch_size

# ----------------------------
# Logging & Retention
# ----------------------------
LOG_HISTORY_SIZE = 0

# ----------------------------
# Evaluated LLMs Registry: Identifiers (legacy — YAML is the registry)
# ----------------------------
# Code should resolve model availability/IDs from YAML at runtime.
GPT_4O = "gpt-4o"                      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Defined in config/models.yaml
GPT_35_TURBO = "gpt-3.5-turbo"         # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Defined in config/models.yaml
GEMINI_1_5_PRO = "gemini-1.5-pro"      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Defined in config/models.yaml
GEMINI_1_5_FLASH = "gemini-1.5-flash"  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Defined in config/models.yaml
GEMINI_2_5_PRO = "gemini-2.5-pro"      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Defined in config/models.yaml
MISTRAL_7B_INSTRUCT = "mistral-7b-instruct"  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Defined in config/models.yaml

# ----------------------------
# Models Enabled/Disabled for Benchmark (legacy — use YAML `enabled:` instead)
# ----------------------------
DISABLED_BENCHMARK_MODELS = {          # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use models.*.enabled in YAML
    GEMINI_2_5_PRO,                    # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Disabled via YAML
}