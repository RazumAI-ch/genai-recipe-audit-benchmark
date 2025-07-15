# File: scripts/train_lora/train_tinyllama_lora.py

print("🚀 Starting TinyLlama LoRA training...")

import argparse
import os
import platform
import shutil
import torch
from datetime import datetime
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
    prepare_model_for_kbit_training
)
from trl import SFTTrainer

# Detect platform
platform_info = platform.system()
hostname = platform.node()
is_mac = platform_info == "Darwin"

# Detect device
if torch.cuda.is_available():
    device_name = torch.cuda.get_device_name(0)
    device_type = "GPU"
    memory_gb = round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
else:
    device_name = platform.processor() or "CPU"
    device_type = "CPU"
    memory_gb = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1e9, 1) if hasattr(os, 'sysconf') else "unknown"

print(f"🖥️ Platform: {platform_info} ({hostname})")
print(f"🧠 Device: {device_type} - {device_name} ({memory_gb} GB)")

# CLI args
parser = argparse.ArgumentParser()
parser.add_argument("--cpu-friendly", action="store_true", help="Enable 4-bit quantization for CPU or low-RAM training")
args = parser.parse_args()

# LoRA config
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Optional quantization config
bnb_config = None
if args.cpu_friendly:
    from transformers import BitsAndBytesConfig
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True
    )
    print("🧠 CPU-friendly 4-bit quantization enabled.")
else:
    print("🚀 Full precision (GPU-optimized) training.")

# Load model and tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config if bnb_config else None
)
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

# Load dataset
dataset = load_dataset("json", data_files="training_data/training_export_*.jsonl", split="train")

# Tokenize in batches
def tokenize(batch):
    return tokenizer(
        [p + "\n" + r for p, r in zip(batch["prompt"], batch["response"])],
        truncation=True,
        padding="max_length",
        max_length=512
    )

tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=dataset.column_names)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Output dir
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
output_dir = f"models/lora_adapters/tinyllama-alcoa-{timestamp}"

# Training args
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=2,
    learning_rate=2e-4,
    bf16=False,
    fp16=False,
    logging_dir="./logs",
    report_to="none"
)

# Launch training
trainer = SFTTrainer(
    model=model,
    train_dataset=tokenized_dataset,
    args=training_args,
    data_collator=data_collator
)

trainer.train()
model.save_pretrained(output_dir)
print(f"✅ LoRA adapter saved to: {output_dir}")

# Archive adapter directory
archive_path = shutil.make_archive(base_name=output_dir, format='gztar', root_dir=output_dir)
print(f"📦 Archive created: {archive_path}")

# Automatically delete archive if running on a Mac
if is_mac:
    try:
        os.remove(archive_path)
        print(f"🧹 Auto-deleted archive (Mac-only): {archive_path}")
    except Exception as e:
        print(f"⚠️ Could not delete archive: {e}")