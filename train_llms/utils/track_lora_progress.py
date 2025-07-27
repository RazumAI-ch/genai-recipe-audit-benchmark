# File: train_llms/utils/track_lora_progress.py

import time
import re
from datetime import datetime, timedelta
from pathlib import Path

log_symlink = Path("../../archive/logs/archivable/llm_training/lora/latest.log")
pattern = re.compile(r"(\d+)/(\d+) \[\d+:\d+<([\d:]+), [\d.]+s/it\]")

def parse_eta_line(line):
    match = pattern.search(line)
    if not match:
        return None
    step, total, eta_str = match.groups()
    step = int(step)
    total = int(total)
    eta_parts = [int(p) for p in eta_str.split(":")]
    eta_seconds = timedelta(
        hours=eta_parts[0], minutes=eta_parts[1], seconds=eta_parts[2]
    ).total_seconds()
    finish_time = datetime.now() + timedelta(seconds=eta_seconds)
    return {
        "step": step,
        "total": total,
        "percent": round((step / total) * 100, 2),
        "eta_str": eta_str,
        "finish_time": finish_time.strftime("%Y-%m-%d %H:%M"),
    }

def resolve_latest_log():
    if not log_symlink.exists():
        print("⏳ Waiting for latest.log to be created...")
        while not log_symlink.exists():
            time.sleep(1)
    if log_symlink.is_symlink() or log_symlink.is_file():
        real_path = log_symlink.resolve()
        print(f"📄 Resolved latest.log to: {real_path}")
        return real_path
    raise FileNotFoundError("❌ latest.log is not a file or symlink.")

def tail_log(file_path):
    print(f"⏳ Tracking LoRA llm_training progress from: {file_path}")
    with open(file_path, "r") as f:
        f.seek(0, 2)  # jump to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            result = parse_eta_line(line)
            if result:
                print(
                    f"📈 Step {result['step']}/{result['total']} "
                    f"({result['percent']}%) — ETA: {result['eta_str']} — "
                    f"Finish: {result['finish_time']}"
                )

if __name__ == "__main__":
    try:
        resolved_log = resolve_latest_log()
        tail_log(resolved_log)
    except Exception as e:
        print(f"❌ Error: {e}")