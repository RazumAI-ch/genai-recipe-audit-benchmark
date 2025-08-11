# File: config/keys_evaluated_llms.py
# ============================
# Canonical keys, provider IDs, and minimal helpers (lean by design)
# ============================

# ---- Canonical model identifiers (must match models.yaml `model` values exactly)
class LLMModels:
    GPT_4O = "gpt-4o"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    MISTRAL_7B_INSTRUCT_V0_3 = "Mistral-7B-Instruct-v0.3"
    GEMINI_2_5_PRO = "gemini-2.5-pro"

    @classmethod
    def all(cls):
        return {value for key, value in cls.__dict__.items()}


# ---- Provider identifiers (must match models.yaml provider keys exactly)
class LLMProviders:
    OPENAI = "OPENAI"
    GEMINI_STUDIO = "GEMINI_STUDIO"
    VERTEX_AI = "VERTEX_AI"
    VULTR = "VULTR"

    @classmethod
    def all(cls):
        return {value for key, value in cls.__dict__.items()}

    @classmethod
    def to_api_key_env(cls, provider: str) -> str:
        """Construct environment variable name for an API key from a provider key."""
        if provider not in cls.all():
            raise ValueError(f"Unknown provider '{provider}'. Expected one of: {sorted(cls.all())}")
        return f"{provider}_API_KEY"


# ---- YAML field names (single source of truth used across loaders/factories)
class YAMLKeys:
    PROVIDER = "provider"
    MODEL = "model"
    ENABLED = "enabled"
    TEMPERATURE = "temperature"
    MAX_TOKENS = "max_tokens"
    BATCH_SIZE = "batch_size"


# ---- Prompts (shared keys for any prompt-bearing configs)
class PromptKeys:
    SYSTEM_PROMPT = "system_prompt"
    USER_PROMPT = "user_prompt"


# ---- Logging & Retention (used by current implementation)
class LogKeys:
    LOG_HISTORY_SIZE = 0


# ---------------------------------------------------------------------------
# Legacy duplicates (flat constants) — keep during migration, remove after 1.0.0
# ---------------------------------------------------------------------------

# YAML keys (legacy flat constants)
PROVIDER = "provider"        # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use YAMLKeys.PROVIDER
MODEL = "model"              # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use YAMLKeys.MODEL
ENABLED = "enabled"          # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use YAMLKeys.ENABLED
TEMPERATURE = "temperature"  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use YAMLKeys.TEMPERATURE
MAX_TOKENS = "max_tokens"    # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use YAMLKeys.MAX_TOKENS
BATCH_SIZE = "batch_size"    # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use YAMLKeys.BATCH_SIZE

# Prompt keys (legacy flat constants)
SYSTEM_PROMPT = "system_prompt"  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use PromptKeys.SYSTEM_PROMPT
USER_PROMPT = "user_prompt"      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use PromptKeys.USER_PROMPT

# Logging (legacy flat constant)
LOG_HISTORY_SIZE = 0             # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use LogKeys.LOG_HISTORY_SIZE



# ---------------------------------------------------------------------------
# Legacy constants to be removed after migration to YAML-only config
# ---------------------------------------------------------------------------

# ---- Env var key (legacy during migration; env var will be constructed from provider)
API_KEY_ENV = "api_key_env"  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Construct from provider via {PROVIDER}_API_KEY

# ---- Legacy global defaults (kept until YAML-only cutover)
LLM_TEMPERATURE = 0.0                 # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use global_model_defaults.temperature
LLM_MAX_TOKENS_DEFAULT = 16000        # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use global_model_defaults.max_tokens
LLM_DEFAULT_BATCH_SIZE = 100          # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use provider_defaults.*.batch_size

# ---- Model identifiers (legacy — defined in YAML; retained for migration)
GPT_4O = "gpt-4o"                      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
GPT_35_TURBO = "gpt-3.5-turbo"         # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
GEMINI_1_5_PRO = "gemini-1.5-pro"      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
GEMINI_1_5_FLASH = "gemini-1.5-flash"  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
GEMINI_2_5_PRO = "gemini-2.5-pro"      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
MISTRAL_7B_INSTRUCT = "mistral-7b-instruct"  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0

# ---- Models Enabled/Disabled for Benchmark (legacy — use YAML `enabled:` instead)
DISABLED_BENCHMARK_MODELS = {          # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use models.*.enabled in YAML
    GPT_35_TURBO,        # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
    GEMINI_1_5_PRO,     # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
    GEMINI_1_5_FLASH,  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
    GEMINI_2_5_PRO,      # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
    MISTRAL_7B_INSTRUCT,  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0
}