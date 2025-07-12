# File: config/loader.py

import yaml

def load_prompt_config(path: str = "config/prompts.yaml") -> dict:
    """
    Load system and user prompt strings from YAML config.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)