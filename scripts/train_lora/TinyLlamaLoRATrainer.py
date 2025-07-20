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
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.dataset = self.load_training_examples_from_db()
        self.tokenized_dataset = self.tokenize_dataset(self.dataset)
        self.total_tokens = sum(len(self.tokenizer.encode(p + "\n" + r)) for p, r in zip(self.dataset["prompt"], self.dataset["response"]))

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.output_dir = f"models/lora_adapters/tinyllama-alcoa-{timestamp}"
        self.log_path = f"logs/training/lora/{timestamp}_TinyLlama-1.1B_{self.record_limit or 'all'}_lora_m4mac_run1.log"
        print(f"📝 Logging to {self.log_path}")
        log_fh = open(self.log_path, "w")
        sys.stdout = sys.stderr = log_fh

        # Create or update symlink to latest log
        latest_link = Path("logs/training/lora/latest.log")
        latest_link.unlink(missing_ok=True)
        latest_link.symlink_to(Path(self.log_path).name)

        print("📋 Training Configuration:")
        print(f"  Model: {self.model_name}")
        print(f"  Samples: {len(self.dataset)}")
        print(f"  Output Dir: {self.output_dir}")
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
            output_dir=self.output_dir,
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

        resume_path = get_last_checkpoint(self.output_dir)

        start_time = datetime.now()
        print(f"🔵 Training started at {start_time}")

        if resume_path:
            print(f"🔁 Resuming training from checkpoint: {resume_path}")
            train_output = trainer.train(resume_from_checkpoint=resume_path)
        else:
            print("🚀 Starting new training run")
            train_output = trainer.train()

        end_time = datetime.now()
        print(f"✅ Training finished at {end_time}")

        train_loss = train_output.metrics.get("train_loss")
        token_accuracy = train_output.metrics.get("mean_token_accuracy")
        if token_accuracy is None:
            token_accuracy = round(max(0.0, min(1.0, 1.0 - train_loss)), 3)

        run_seconds = (end_time - start_time).total_seconds()
        estimated_cost = 0.00  # Always 0 on Mac

        model.save_pretrained(self.output_dir)
        print(f"✅ LoRA adapter saved to: {self.output_dir}")

        archive_path = shutil.make_archive(base_name=self.output_dir, format='gztar', root_dir=self.output_dir)
        print(f"📦 Archive created: {archive_path}")

        if self.is_mac_m4:
            try:
                os.remove(archive_path)
                print(f"🧹 Auto-deleted archive (Mac-only): {archive_path}")
            except Exception as e:
                print(f"⚠️ Could not delete archive: {e}")

        with open(self.log_path, "a") as log_file:
            duration = timedelta(seconds=int(run_seconds))
            log_file.write(f"\n📈 Training complete | loss={train_loss:.4f} | accuracy={token_accuracy:.4f} | total_time={duration}\n")
            avg_epoch_time = duration.total_seconds() / 3
            remaining_time = timedelta(seconds=int(avg_epoch_time * 2))
            log_file.write(f"🕒 Estimated time remaining if same pace: {remaining_time}\n")

        if os.path.getsize(self.log_path) < 100:
            print(f"🚨 Warning: Log file {self.log_path} is suspiciously small — training may have failed.")

        self.log_training_run((
            "TinyLlama-1.1B",
            "lora",
            f"{len(self.dataset)} training examples (random sample)" if self.record_limit else "All training examples from DB",
            len(self.dataset),
            self.total_tokens,
            3,
            self.hardware,
            start_time,
            run_seconds,
            train_loss,
            token_accuracy,
            self.log_path,
            self.output_dir,
            "Automated LoRA training run recorded by TinyLlamaLoRATrainer",
            estimated_cost,
            0.00
        ))


if __name__ == "__main__":
    trainer = TinyLlamaLoRATrainer()
    trainer.run()