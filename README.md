# 🧪 GenAI Recipe Audit Benchmark

A reproducible benchmark for evaluating how well large language models identify, classify, and explain GxP-relevant deviations in pharmaceutical manufacturing recipes. Designed for regulatory-grade infrastructure auditing with both proprietary and open models.

---

## 🎯 Project Goals

- Evaluate generalization of LLMs to regulated pharmaceutical auditing
- Measure impact of LoRA and full retraining on deviation detection
- Compare cost-effectiveness and speed per model
- Build reproducible scientific infrastructure for regulatory-grade evaluation

---

## 🔧 Capabilities

- Generate synthetic recipe samples with injected, documented ALCOA+ deviations (2% of records)
- Evaluate across top LLMs (OpenAI, Claude, Gemini, Mistral, etc.)
- Benchmark both open and fine-tuned models
- Score detection and classification performance per model
- Fully reproducible with Docker + PostgreSQL + Makefile

---

## 📋 GxP Benchmark Overview

This project provides an end-to-end benchmark to evaluate how well generative AI models identify GxP-relevant deviations in pharmaceutical manufacturing recipes. Our focus is on six scoring dimensions:

| Score     | Scope                                                | Availability  |
|-----------|------------------------------------------------------|---------------|
| **GxP1**  | ALCOA+ violation identification                      | ✅ Open source |
| **GxP2**  | ALCOA+ violation classification                      | ✅ Open source |
| **GxP3**  | Recipe logic consistency deviation identification    | 🔒 Commercial  |
| **GxP4**  | Recipe logic consistency deviation classification    | 🔒 Commercial  |
| **GxP5**  | Execution trace deviation identification             | 🔒 Commercial  |
| **GxP6**  | Execution trace deviation classification             | 🔒 Commercial  |

---

## 📊 GxP1 & GxP2 Scoring Explained

The benchmark dataset is synthetically generated in a controlled way. We know exactly:

- Which records are clean
- Which records contain deviations
- Which specific deviation types were injected into which records

There are 30 deviation types including:

- Missing quantity  
- Invalid timestamp format  
- Placeholder text  
- Out-of-sequence steps  
- Unauthorized entries  
- Invalid equipment IDs

Full list available in `config/deviation_types.csv`.

---

## 📂 Project Structure

```
genai-recipe-audit-benchmark/
├── archive/         # Backups of DB and logs
├── benchmark_llms/  # Core benchmark runner and scoring logic
├── config/          # Prompt templates and LLM pricing
├── db/              # Production DB access layer
├── docs/            # Usage and methodology
├── llms/            # LLM wrappers (API, open, and retrained)
├── loggers/         # Structured log generation for benchmarks/tests
├── models/          # Saved LoRA adapter folders and full retrain outputs
├── public_assets/   # Public media, reports, or charts
├── train_llms/      # Training logic (LoRA or full)
├── unit_tests/      # Unit test runner and test-only DB access
├── main.py          # Benchmark entry point
├── Makefile         # Unified execution interface
├── requirements.txt # Python dependencies
```

---

## 🧠 LLM Integration

### Proprietary Models (API-Based Inference Only)

- OpenAI GPT-4o
- Claude Opus
- Gemini 1.5 Pro

Planned:
- Claude 3.5 Sonnet
- Cohere Command R+
- xAI Grok
- Mistral API models

### Open-Source Models (Inference Only)

- LLaMA-3 8B / 70B
- Mixtral 8x7B
- Gemma 2B / 7B
- Phi-2
- Qwen 1.5 14B / 72B / 110B
- Yi-6B / Yi-34B
- Mistral 7B Instruct
- Command R / R+ (open)
- TinyLlama 1.1B
- LLaMA-3 400B / 460B (planned)

### LoRA-Tuned Models

- TinyLlama 1.1B (already trained)
- Phi-2
- Gemma 2B / 7B
- Qwen 7B / 14B
- Yi 6B / 34B
- Mistral 7B
- Mixtral 8x7B

### Full Retraining (Selective)

- TinyLlama 1.1B (baseline done)
- Phi-2
- Possibly: Qwen 7B or Yi 6B

---

## 🎓 Testing & DB Validation

This project includes a suite of unit tests to validate infrastructure health, schema alignment, and data quality. These include:

- `schema_docs_sync`: Ensures all DB columns are documented in `schema_docs`
- `psqldb_sequences`: Validates that all sequences are synchronized with `MAX(id) + 1`

Run tests with:

```bash
make _run-unit-tests
```

All results are logged to timestamped files.

---

## 📊 Cost Monitoring

All benchmarks track:

- API usage and token cost
- Runtime per model
- Score per run

---

## 🚀 Run Locally

```bash
docker-compose up -d
make setup-db
python main.py
```

---

## 🛠 Tech Stack

### Core Language
- Python 3.11

### Database
- PostgreSQL 15
- SQLAlchemy (ORM layer)
- Psycopg2 (direct SQL access)

### Deployment & Orchestration
- Docker
- Makefile

### LLM Integration
- OpenAI, Claude, Gemini (API-based proprietary models)
- TinyLlama 1.1B (LoRA fine-tuned open model)

---

## 📑 Licensing & Reuse

- GxP1 and GxP2 logic is fully open-source
- GxP3–6 logic is commercial due to proprietary execution trace data

---

## 🏁 Final Notes

- All deviation types are explicitly tied to ALCOA+ principles
- Benchmark is reproducible, automatable, and extensible
- Unit tests enforce schema documentation and DB integrity prior to benchmark execution