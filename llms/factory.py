# File: llms/factory.py

import typing
import config.keys
import llms.model_openai as model_openai

# Define which models are currently enabled for evaluation
ENABLED_MODELS = {
    config.keys.OPENAI_GPT_4O,
    # Add other model keys here when ready
}

# Registry of all known models mapped to their implementation class
MODEL_REGISTRY = {
    config.keys.OPENAI_GPT_4O: model_openai.OpenAIModel,
    # config.keys.OPENAI_GPT_4: model_openai.OpenAIModel,
    # config.keys.CLAUDE_OPUS: model_claude.ClaudeModel,
    # config.keys.GEMINI_1_5_PRO: model_gemini.GeminiModel,
}

def get_enabled_models() -> typing.Dict[str, typing.Type]:
    """
    Returns a filtered version of the model registry that includes only enabled models.
    """
    return {k: v for k, v in MODEL_REGISTRY.items() if k in ENABLED_MODELS}

def load_model(model_name: str, overrides: typing.Dict[str, typing.Any] = None):
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

    model = model_class()
    model.prepare(overrides=overrides)
    return model