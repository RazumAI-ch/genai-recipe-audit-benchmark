# File: scripts/utils/logging.py

import os
from datetime import datetime
from config.paths import PATH_LOGS_DEBUG

def save_raw_response(content: str, model_name: str = "unknown") -> str:
    """
    Save raw model output to a timestamped file for debugging.

    Clears existing debug files before saving a new one.

    Parameters:
    - content: the raw text (typically a JSON string)
    - model_name: optional name of the model (used in filename)

    Returns:
    - The full path of the file saved.
    """
    debug_dir = PATH_LOGS_DEBUG
    os.makedirs(debug_dir, exist_ok=True)

    # 🧹 Delete old files before saving
    for fname in os.listdir(debug_dir):
        file_path = os.path.join(debug_dir, fname)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"⚠️ Could not delete file: {file_path} — {e}")

    # 💾 Save new response
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{debug_dir}/response_{model_name}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename