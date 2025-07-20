# utils.py
# Shared utility functions like file reading and cost estimation.

import re


def estimate_cost(num_tokens: int, model: str) -> float:
    """
    Estimate the cost of processing tokens for a specific model.
    """
    if model.startswith("gpt-3.5"):
        price_per_1k = 0.001  # USD per 1K tokens (input only)
    elif model.startswith("gpt-4o"):
        price_per_1k = 0.005  # USD per 1K tokens (input only)
    else:
        price_per_1k = 0.01  # fallback/default for unknown models

    return round((num_tokens / 1000) * price_per_1k, 4)


def extract_file_metadata(uploaded_file, content_bytes):
    """
    Extract filename, content as a string, and file extension.
    Used when handling uploaded files.
    """
    filename = uploaded_file.name
    file_extension = filename.split(".")[-1].lower()
    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        content_str = content_bytes.decode("latin1")  # fallback for non-UTF-8 encodings
    return filename, content_str, file_extension


def extract_file_content(uploaded_file):
    """
    Read and decode file contents as bytes and UTF-8 string.
    """
    content_bytes = uploaded_file.read()
    content_str = content_bytes.decode("utf-8")
    return content_bytes, content_str


def detect_file_type(file_name: str) -> str:
    """
    Determine whether the file is JSON, CSV, or unknown.
    """
    if file_name.endswith(".json"):
        return "json"
    elif file_name.endswith(".csv"):
        return "csv"
    else:
        return "unknown"


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON object from text that may include Markdown fences.
    - If text starts with '{', assume it is plain JSON.
    - If wrapped in ```json ... ```, extract the inner content.
    """
    if text.strip().startswith("{"):
        return text.strip()

    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    return text.strip()
