# File: scripts/BaseTrainer.py

import os
import platform
import psycopg2
from datetime import datetime
from pathlib import Path
import pytz
import torch

class BaseTrainer:
    def __init__(self):
        raw_hw = input("💻 Use GPU (press Enter) or run on Mac M4 Max (type 'm')? ").strip().lower()
        self.is_mac_m4 = raw_hw == "m"
        self.hardware = "MacBook Pro M4 Max (128 GB)" if self.is_mac_m4 else self.detect_hardware()
        self.db_connected = False
        self.conn = None
        self.total_records = 0
        self.record_limit = 0
        self.try_connect_to_db()
        self.record_limit = self.prompt_record_limit()

        # Use CET timezone for consistency
        cet = pytz.timezone("CET")
        self.start_time = datetime.now(cet)
        self.timestamp = self.start_time.strftime('%Y-%m-%d_%H-%M')

        self.output_dir = f"models/lora_adapters/{self.timestamp}_adapter"
        # self.log_path must now be set by subclass

    def try_connect_to_db(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                dbname=os.getenv("DB_NAME", "benchmarkdb"),
                user=os.getenv("DB_USER", "benchmark"),
                password=os.getenv("DB_PASSWORD", "benchmark"),
                port=os.getenv("DB_PORT", "5432")
            )
            with self.conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM training_examples;")
                self.total_records = cur.fetchone()[0]
            self.db_connected = True
            print("✅ Database connection verified.")
        except Exception as e:
            print("⚠️ Could not connect to DB. Training will proceed without DB access.")
            print(str(e))
            self.db_connected = False
            self.total_records = 0

    def prompt_record_limit(self):
        if self.db_connected:
            print(f"📊 Total llm_training examples available in DB: {self.total_records}")
        else:
            print("📊 DB is offline — llm_training will load 0 records unless overridden manually.")
        raw = input("🔢 How many examples do you want to load? (press Enter to load all): ").strip()
        try:
            if raw == "" or raw == "-1":
                if self.db_connected:
                    print("📅 Loading all available records.")
                    return None
                else:
                    raise RuntimeError("❌ Cannot load all records — DB is unavailable.")
            val = int(raw)
            if val <= 0 or (self.db_connected and val > self.total_records):
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

    def symlink_latest_log(self, log_path: str):
        latest_symlink = Path("../logs/archivable/llm_training/lora/latest.log")
        target_path = Path(log_path)

        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.touch(exist_ok=True)
            if latest_symlink.exists() or latest_symlink.is_symlink():
                latest_symlink.unlink()

            try:
                relative_target = target_path.relative_to(Path.cwd())
                latest_symlink.symlink_to(relative_target)
            except ValueError:
                latest_symlink.symlink_to(target_path)

            print(f"🔗 latest.log now points to: {latest_symlink.resolve()}")
        except Exception as e:
            print(f"⚠️ Could not create latest.log symlink: {e}")

    def run(self):
        raise NotImplementedError("Subclasses must implement the run() method.")