# File: config/keys_providers.py
# ============================
# Canonical keys for provider configs (single source of truth)
# ============================

class ProviderYAMLKeys:
    BASE_URL = "base_url"
    HTTP = "http"
    HTTP_TIMEOUT = "timeout_seconds"
    HTTP_MAX_RETRIES = "max_retries"
    HTTP_RATE_SLEEP = "rate_limit_sleep"
    MODEL_OVERRIDES = "model_overrides"
    ENDPOINT_MODEL_ID = "endpoint_model_id"


class LLMProviders:
    OPENAI = "OPENAI"
    GEMINI_STUDIO = "GEMINI_STUDIO"
    VERTEX_AI = "VERTEX_AI"
    VULTR = "VULTR"

    @classmethod
    def all(cls):
        # Only uppercase string fields (prevents methods/classes from leaking in)
        return {
            v for k, v in cls.__dict__.items()
            if k.isupper() and isinstance(v, str)
        }

    @classmethod
    def to_api_key_env(cls, provider: str) -> str:
        """Construct environment variable name for an API key from a provider key."""
        if provider not in cls.all():
            raise ValueError(f"Unknown provider '{provider}'. Expected one of: {sorted(cls.all())}")
        return f"{provider}_API_KEY"