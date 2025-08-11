# File: benchmark_llms/evaluated_llms/utils/response_utils.py
from __future__ import annotations
import json
import benchmark_llms.evaluated_llms.utils.utils as text_utils

def parse_model_response(content: str) -> dict:
    if not content:
        raise ValueError("Empty response from LLM.")
    clean = text_utils.extract_json_from_text(content)
    if not clean.strip().startswith(("{", "[")):
        raise ValueError(f"Cleaned response is not valid JSON. Starts with: {clean.strip()[:60]!r}")
    parsed = json.loads(clean)
    if isinstance(parsed, list):
        parsed = {"summary_text": "", "records": parsed}
    parsed.setdefault("summary_text", "")
    return parsed