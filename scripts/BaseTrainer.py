# File: scripts/BaseTrainer.py

import os
import platform
import psycopg2
from datetime import datetime
from pathlib import Path
import torch

class BaseTrainer:
    def __init__(self):
        raw_hw = input("💻 Use GPU (press Enter) or run on Mac M4 Max (type 'm')? ").strip().lower()
        self.is_mac_m4 = raw_hw == "m"
        self.hardware = "MacBook Pro M4 Max (128 GB)" if self.is_mac_m4 else self.detect_hardware()
        self.conn = self.connect_to_db()
        self.cur = self.conn.cursor()
        self.total_records = self.fetch_total_record_count()
        self.record_limit = self.prompt_record_limit()
        self.start_time = datetime.now()
        self.timestamp = self.start_time.strftime('%Y-%m-%d_%H-%M')
        self.output_dir = f"models/lora_adapters/{self.timestamp}_adapter"
        self.log_path = f"logs/training/lora/{self.timestamp}_train.log"
        self.symlink_latest_log()

    def connect_to_db(self):
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            dbname=os.getenv("DB_NAME", "benchmarkdb"),
            user=os.getenv("DB_USER", "benchmark"),
            password=os.getenv("DB_PASSWORD", "benchmark"),
            port=os.getenv("DB_PORT", "5432")
        )

    def fetch_total_record_count(self):
        self.cur.execute("SELECT COUNT(*) FROM training_examples;")
        return self.cur.fetchone()[0]

    def prompt_record_limit(self):
        print(f"📊 Total training examples available in DB: {self.total_records}")
        raw = input("🔢 How many examples do you want to load? (press Enter to load all): ").strip()
        try:
            if raw == "" or raw == "-1":
                print("📅 Loading all available records.")
                return None
            val = int(raw)
            if val <= 0 or val > self.total_records:
                raise ValueError
            print(f"📅 Loading {val} randomly selected records.")
            return val
        except ValueError:
            raise RuntimeError("❌ Invalid input. Please enter a positive number or press Enter to load all.")

    def detect_hardware(self):
        platform_info = platform.system()
        hostname = platform.node()
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            memory_gb = round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
            device_type = "GPU"
        else:
            device_name = platform.processor() or "CPU"
            memory_gb = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1e9, 1) if hasattr(os, 'sysconf') else "unknown"
            device_type = "CPU"
        return f"{device_type} - {device_name} ({memory_gb} GB), running on {platform_info} ({hostname})"

    def symlink_latest_log(self):
        latest_symlink = Path("logs/training/lora/latest.log")
        target_path = Path(self.log_path)

        try:
            # Ensure log directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Ensure log file exists (creates an empty one if needed)
            target_path.touch(exist_ok=True)

            # Remove old symlink if it exists
            if latest_symlink.exists() or latest_symlink.is_symlink():
                latest_symlink.unlink()

            # Try relative symlink (host-safe), fallback to absolute (container-safe)
            try:
                relative_target = target_path.relative_to(Path.cwd())
                latest_symlink.symlink_to(relative_target)
            except ValueError:
                latest_symlink.symlink_to(target_path)

            print(f"🔗 latest.log now points to: {latest_symlink.resolve()}")
        except Exception as e:
            print(f"⚠️ Could not create latest.log symlink: {e}")

    def log_training_run(self, metadata):
        self.cur.execute("""
            INSERT INTO training_runs (
                model_name, method, dataset_description, total_samples, total_tokens, epochs,
                hardware, start_time, duration_seconds, final_loss, final_accuracy,
                log_path, model_output_path, notes, cost_usd, gpu_cost_per_hour
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, metadata)
        training_run_id = self.cur.fetchone()[0]
        self.conn.commit()
        print(f"🗃️  Training run recorded in DB (ID = {training_run_id})")

    def run(self):
        raise NotImplementedError("Subclasses must implement the run() method.")