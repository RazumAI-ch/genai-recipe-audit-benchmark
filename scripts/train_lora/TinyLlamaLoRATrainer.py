# File: scripts/train_lora/TinyLlamaLoRATrainer.py

from scripts.BaseTrainer import BaseTrainer
import os
import sys
import torch
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
    prepare_model_for_kbit_training
)
from trl import SFTTrainer
from transformers.trainer_utils import get_last_checkpoint
import transformers.trainer
transformers.trainer.logger.setLevel("INFO")


class TinyLlamaLoRATrainer(BaseTrainer):
    def __init__(self):
        torch.set_num_threads(os.cpu_count())
        print(f"🧵 PyTorch threads set to: {torch.get_num_threads()}")
        super().__init__()
        self.model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.model_size = "1.1b"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.dataset = self.load_training_examples_from_db()
        self.tokenized_dataset = self.tokenize_dataset(self.dataset)
        self.total_tokens = sum(len(self.tokenizer.encode(p + "\n" + r)) for p, r in zip(self.dataset["prompt"], self.dataset["response"]))

        sample_count = len(self.dataset)
        sample_label = f"{sample_count}"
        hardware_label = "m4mac" if self.is_mac_m4 else "a100"
        self.base_name = f"{self.timestamp}_tinyllama-{self.model_size}-{sample_label}-{hardware_label}"

        self._temp_output_dir = f"models/lora_adapters/tmp-{self.base_name}"
        self.final_output_dir = f"models/lora_adapters/{self.base_name}"
        self.archive_path = f"models/lora_adapters/_archives/{self.base_name}.tar.gz"
        self.log_path = f"logs/training/lora/{self.base_name}.log"

        print(f"📝 Logging to {self.log_path}")
        log_fh = open(self.log_path, "w")
        sys.stdout = sys.stderr = log_fh

        self.symlink_latest_log(self.log_path)

        print("📋 Training Configuration:")
        print(f"  Model: {self.model_name}")
        print(f"  Samples: {sample_count}")
        print(f"  Output Dir (temp): {self._temp_output_dir}")
        print(f"  Log File: {self.log_path}")
        print(f"  Platform: macOS | Hardware: {self.hardware} | Full Power Mode: {'Yes' if self.is_mac_m4 else 'No'}")

    def load_training_examples_from_db(self):
        cur = self.conn.cursor()
        cur.execute(f"""
            SELECT input_content
            FROM training_examples
            {'ORDER BY RANDOM() LIMIT %s' if self.record_limit else ''};
        """, (self.record_limit,) if self.record_limit else ())
        rows = cur.fetchall()
        data = [{"prompt": row[0], "response": ""} for row in rows]
        cur.close()
        return Dataset.from_list(data)

    def tokenize_dataset(self, dataset):
        def tokenize(batch):
            return self.tokenizer(
                [p + "\n" + r for p, r in zip(batch["prompt"], batch["response"])],
                truncation=True,
                padding="max_length",
                max_length=512
            )
        return dataset.map(tokenize, batched=True, remove_columns=dataset.column_names)

    def run(self):
        from transformers.trainer import Trainer
        _original_get_train_dataloader = Trainer.get_train_dataloader

        def _patched_get_train_dataloader(self_):
            dataloader = _original_get_train_dataloader(self_)
            dataloader.pin_memory = False
            return dataloader

        Trainer.get_train_dataloader = _patched_get_train_dataloader

        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )

        bnb_config = None
        if self.is_mac_m4:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True
            )
            print("🧠 CPU-friendly 4-bit quantization enabled.")
        else:
            print("🚀 Full precision (GPU-optimized) training.")

        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            quantization_config=bnb_config
        )
        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, lora_config)

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

        training_args = TrainingArguments(
            output_dir=self._temp_output_dir,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            num_train_epochs=3,
            logging_steps=10,
            save_strategy="steps",
            save_steps=100,
            save_total_limit=5,
            learning_rate=2e-4,
            bf16=False,
            fp16=False,
            logging_dir="./logs",
            report_to="none",
            gradient_checkpointing=True,
            gradient_checkpointing_kwargs={"use_reentrant": False}
        )

        trainer = SFTTrainer(
            model=model,
            train_dataset=self.tokenized_dataset,
            args=training_args,
            data_collator=data_collator
        )

        resume_path = get_last_checkpoint(self._temp_output_dir)

        print(f"🔵 Training started at {self.start_time}")

        if resume_path:
            print(f"🔁 Resuming training from checkpoint: {resume_path}")
            train_output = trainer.train(resume_from_checkpoint=resume_path)
        else:
            print("🚀 Starting new training run")
            train_output = trainer.train()

        print(f"DEBUG: train_output = {train_output}")
        print(f"DEBUG: train_output.metrics = {getattr(train_output, 'metrics', None)}")

        if not train_output or not getattr(train_output, "metrics", None):
            print("⚠️ WARNING: train_output or metrics missing — using defaults.")
            train_loss = 0.0
            token_accuracy = 0.0
        else:
            metrics = train_output.metrics
            train_loss = metrics.get("train_loss", 0.0)
            token_accuracy = metrics.get("mean_token_accuracy")
            if token_accuracy is None:
                token_accuracy = round(max(0.0, min(1.0, 1.0 - train_loss)), 3)

        end_time = datetime.now()
        run_seconds = (end_time - self.start_time).total_seconds()
        estimated_cost = 0.00

        model.save_pretrained(self._temp_output_dir)
        print(f"✅ LoRA adapter saved to: {self._temp_output_dir}")

        shutil.move(self._temp_output_dir, self.final_output_dir)

        archive_dir = Path(self.archive_path).parent
        archive_dir.mkdir(exist_ok=True)
        shutil.make_archive(
            base_name=self.archive_path.replace(".tar.gz", ""),
            format="gztar",
            root_dir=self.final_output_dir
        )
        print(f"📦 Archive created: {self.archive_path}")

        with open(self.log_path, "a") as log_file:
            duration = timedelta(seconds=int(run_seconds))
            log_file.write(f"\n📈 Training complete | loss={train_loss:.4f} | accuracy={token_accuracy:.4f} | total_time={duration}\n")
            log_file.write(f"📦 Output Folder: {self.final_output_dir}\n")
            log_file.write(f"🧾 Training Summary:\n")
            log_file.write(f"  Model: TinyLlama-1.1B\n")
            log_file.write(f"  Method: lora\n")
            log_file.write(f"  Samples: {len(self.dataset)}\n")
            log_file.write(f"  Tokens: {self.total_tokens}\n")
            log_file.write(f"  Hardware: {self.hardware}\n")
            log_file.write(f"  Started: {self.start_time.isoformat()}\n")
            log_file.write(f"  Duration (sec): {int(run_seconds)}\n")
            log_file.write(f"  Train Loss: {train_loss:.4f}\n")
            log_file.write(f"  Accuracy: {token_accuracy:.4f}\n")
            log_file.write(f"  Log File: {self.log_path}\n")
            log_file.write(f"  Cost (USD): {estimated_cost:.2f}\n")


if __name__ == "__main__":
    trainer = TinyLlamaLoRATrainer()
    trainer.run()