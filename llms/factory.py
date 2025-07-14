# File: llms/factory.py

from typing import Dict, Any
from llms.model_openai import OpenAIModel
# from llms.model_claude import ClaudeModel  # To be implemented
# from llms.model_gemini import GeminiModel  # To be implemented
from config.keys import (
    OPENAI_GPT_4O,
    OPENAI_GPT_4,
    OPENAI_GPT_3_5_TURBO,
    # CLAUDE_OPUS,
    # GEMINI_1_5_PRO
)

# 🔁 Registry mapping model keys to concrete LLM classes.
# This allows dynamic lookup and instantiation by model ID.
MODEL_REGISTRY = {
    OPENAI_GPT_4O: OpenAIModel,
    OPENAI_GPT_4: OpenAIModel,
    OPENAI_GPT_3_5_TURBO: OpenAIModel,
    # CLAUDE_OPUS: ClaudeModel,
    # GEMINI_1_5_PRO: GeminiModel
}

def load_model(model_name: str, overrides: Dict[str, Any] = None):
    """
    Instantiate a model class from the registry using the given name.
    Applies optional overrides (e.g., change model version or batch size).

    Args:
        model_name: Key from MODEL_REGISTRY identifying the LLM.
        overrides: Optional dictionary to override config values.

    Returns:
        An initialized and prepared LLM instance.

    Raises:
        ValueError if the model_name is not registered.
    """
    model_class = MODEL_REGISTRY.get(model_name)
    if not model_class:
        raise ValueError(f"Model '{model_name}' is not registered.")

    model = model_class()              # Instantiate class
    model.prepare(overrides=overrides)  # Apply configuration
    return model