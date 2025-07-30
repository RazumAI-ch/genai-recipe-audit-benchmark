# 🧰 Command-Line Interface (CLI) Guide – GenAI Recipe Audit Benchmark

This guide documents how to interact with the project via the command line, including:
- Running the benchmark
- Managing the database
- Generating and inspecting training data
- Training models

---

## ✅ Prerequisites

- Docker installed and available in your terminal
- `make` installed (comes preinstalled on macOS and Linux)
- Project cloned locally

---

## 🚀 Benchmark Execution

| Command             | Description                                                  |
|----------------------|--------------------------------------------------------------|
| `make run`           | Run the benchmark (default mode, uses default record count)  |
| `make run 20`        | Run the benchmark on 20 records                              |
| `make run none`      | Run the benchmark on **all** available sample records        |

> ℹ️ `make run` accepts an optional **positional argument**:  
> - Omit it to use the system default  
> - Use `20` to audit 20 records  
> - Use `none` to process the entire dataset

---

## 💾 Database Management

| Command                          | Description                                                   |
|----------------------------------|---------------------------------------------------------------|
| `make psql`                      | Open a `psql` prompt inside the DB container                  |
| `make backup-db`                 | Recreate DB and restore schema/docs from latest archive       |
| `make import-db-adhoc FILE=...` | Restore DB from a specified `.sql.gz` backup                  |

---

## 🧠 Model Training (LoRA)

| Command                     | Description                                          |
|-----------------------------|------------------------------------------------------|
| `make train-lora-tinyllama` | Run LoRA training locally with TinyLlama             |
| `make tail-lora-log`        | Live tail of the latest training log                |
| `make track-lora-progress`  | View summary stats (accuracy/loss) of last training |

---

## 🏗️ Training Data Management

| Command                                  | Description                                       |
|-------------------------------------------|---------------------------------------------------|
| `make generate-training-examples`        | Generate and insert training records in the DB    |
| `make check-training-data`              | Run all training data checks (below)              |
| `make check-training-examples`          | View last 10 training examples                    |
| `make check-training-example-deviations`| View last 20 deviations linked to training data   |
| `make check-training-llm-sources`       | View source LLMs used for generating examples     |

---

## 📊 Utilities

| Command           | Description                    |
|--------------------|--------------------------------|
| `make docker-stats`| Show container memory/CPU usage|

---

## 📚 See Also

- `README.md` – Project overview and structure
- `db/schema.sql` – Current database schema
- `archive/` – DB and training backups
- `logs/debug/` – LLM responses from benchmark runs

---

## 🛑 Internal Targets (Not for Direct Use)

The following Makefile targets are **internal only**. They are automatically invoked by public commands and should **not** be run manually:

- All targets starting with `_` (e.g., `_wait-for-db`, `_run-unit-tests`, `_refresh-schema-docs`)
- `clear` – used internally to clean the terminal
- `archive-latest-logs` – called by `backup-db`, not for standalone use
- `show-db-stats` – shown automatically as part of other flows