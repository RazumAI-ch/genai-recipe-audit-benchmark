# 🧪 GenAI Recipe Audit Benchmark

Benchmarking GenAI Models for GxP Pharmaceutical Recipe Auditing.

We evaluate how well each individual language model performs in detecting, classifying, and explaining GxP-relevant deviations in structured pharmaceutical manufacturing recipes. All models are tested on the same tasks, using identical prompts and evaluation logic, allowing direct comparison of their performance, cost, and reliability.

---

### 🏢 Proprietary Models (API-Based Inference Only)

These commercial LLMs are accessed via API and evaluated without any retraining:

- **OpenAI GPT-4o**
- **Claude Opus**
- **Gemini 1.5 Pro**

Planned future additions include:

- **Anthropic Claude 3.5 Sonnet**
- **Cohere Command R+**
- **xAI Grok**
- **Mistral API models (as released)**

---

### 🧠 Open-Source Models (Inference Only)

We will benchmark the following open models for out-of-the-box performance on GxP1–2 tasks:

- **LLaMA-3 8B / 70B**
- **Mixtral 8x7B**
- **Gemma 2B / 7B**
- **Phi-2**
- **Qwen 1.5 14B / 72B / 110B**
- **Yi-6B / Yi-34B**
- **Mistral 7B Instruct**
- **Command R / R+ (open variants)**
- **TinyLlama 1.1B**
- **LLaMA-3 400B / 460B** *(for future inference runs)*

---

### 🧪 Planned LoRA-Tuned Models

The following open models are selected for **LoRA fine-tuning** based on practical feasibility under current resource constraints. They strike a balance between performance and retraining cost:

- **TinyLlama 1.1B** *(already trained)*
- **Phi-2**
- **Gemma 2B / 7B**
- **Qwen 7B / 14B**
- **Yi 6B / 34B**
- **Mistral 7B**
- **Mixtral 8x7B**

These will be fine-tuned using 10k+ annotated records to specialize in GxP1 and GxP2 detection and classification.

---

### 🧬 Planned Full Retraining (Selective)

Full retraining is resource-intensive and will be limited to a small number of models:

- **TinyLlama 1.1B** *(baseline completed)*
- **Phi-2**
- Possibly: **Qwen 7B** or **Yi 6B**

These runs will be reserved for future large-scale experiments using dedicated cloud GPU instances or high-memory nodes.

---

## 📋 GxP Benchmark Overview

This project provides an end-to-end benchmark to evaluate how well generative AI models identify **GxP-relevant deviations** in pharmaceutical manufacturing recipes. Our focus is on six scoring dimensions:

| Score     | Scope                                                | Availability  |
|-----------|------------------------------------------------------|---------------|
| **GxP1**  | ALCOA+ violation identification                      | ✅ Open source |
| **GxP2**  | ALCOA+ violation classification                      | ✅ Open source |
| **GxP3**  | Recipe logic consistency deviation identification    | 🔒 Commercial  |
| **GxP4**  | Recipe logic consistency deviation classification    | 🔒 Commercial  |
| **GxP5**  | Execution trace deviation identification             | 🔒 Commercial  |
| **GxP6**  | Execution trace deviation classification             | 🔒 Commercial  |

GxP1–2 are part of the open benchmark. GxP3–6 require access to proprietary process logic and execution logs, and are offered commercially.

---

## 🔧 Capabilities

- ✅ Generate **synthetic recipe samples** with injected, documented ALCOA+ deviations (2% of records)
- ✅ Evaluate across top LLMs (OpenAI, Claude, Gemini, Mistral, etc.)
- ✅ Benchmark both open and fine-tuned models
- ✅ Score detection and classification performance per model
- ✅ Fully reproducible with Docker + PostgreSQL + Makefile

---

## 🎯 Project Goals

- Evaluate generalization of LLMs to regulated pharmaceutical auditing
- Measure impact of LoRA and full retraining on deviation detection
- Compare cost-effectiveness and speed per model
- Build reproducible scientific infrastructure for regulatory-grade evaluation

---

## 📂 Project Structure

```
genai-recipe-audit-benchmark/
├── benchmark/     # Core scoring logic and run orchestration
├── config/        # Prompt templates and pricing info
├── db/            # PostgreSQL schema + seed data
├── docs/          # CLI usage, methodology, and examples
├── llms/          # LLM wrappers (OpenAI, Claude, etc.)
├── models/        # Trained LoRA adapters and fine-tuned models
├── scripts/       # Synthetic data generation and training tools
├── tests/         # Unit and integration tests
└── main.py        # Benchmark entry point
```

---

## 🚀 Run Locally

```bash
docker-compose up -d
make setup-db
python main.py
```

---

## 🧠 LoRA and Full Fine-Tuning

Our training dataset consists of 10,000 structured records annotated with ALCOA+ deviation types. Fine-tuning is optimized for the **GxP1** and **GxP2** tasks.

Training runs are:
- Logged with metadata (time, accuracy, loss, token count)
- Executed via **RunPod**, **AWS**, **Vultr**, or **local hardware**
- Archived with timestamped folders and `.tar.gz` snapshots

---

## 🧪 Benchmark Configuration

Defined in:

- `config/prompts.yaml`: Unified prompt across all models
- `config/model_pricing.yaml`: Token-based cost tracking

Design includes:

- Same prompt for all models
- Structured JSON output
- Normalized scoring [0–1]
- Control datasets (100% clean or 100% faulty)

---

## 📊 GxP1 & GxP2 Scoring Explained

The benchmark dataset is synthetically generated in a controlled way. We know exactly:
- Which records are clean
- Which records contain deviations
- Which specific deviation types were injected into which records

There are **30 deviation types** used to classify issues:

1. Missing quantity  
2. Invalid timestamp format  
3. Future timestamp  
4. Timestamp out of sequence  
5. Invalid status code  
6. Placeholder text in notes  
7. Empty notes field  
8. Overwritten field without comment  
9. Missing operator ID  
10. Invalid operator ID format  
11. Operator mismatch  
12. Duplicate record ID  
13. Negative quantity  
14. Unexpected material usage  
15. Inconsistent unit of measure  
16. Reused batch number  
17. Non-GMP-compliant free text  
18. Timestamp with wrong timezone  
19. Redundant step  
20. Out-of-spec temperature  
21. Out-of-spec duration  
22. Unexpected step order  
23. Missing environmental condition  
24. Extra field not in schema  
25. Misspelled field name  
26. Unauthorized user entry  
27. Data recorded before step start  
28. Data recorded after step end  
29. Zero duration  
30. Invalid equipment ID

---

## 📊 Cost Monitoring

All benchmarks track:

- API usage and token cost
- Runtime per model
- Score per run

---

## 🚚 Deployment Roadmap

- ✅ CLI-based execution (Docker + PostgreSQL)
- 🔜 Web-based interface for running benchmarks and viewing results

---

## 📑 Licensing & Reuse

- GxP1 and GxP2 logic is fully open-source
- GxP3–6 are commercial due to proprietary logic and trace requirements

---

## 🏁 Final Notes

- 📢 Prompts and deviation types are tied to ALCOA+ principles
- 🔍 Each deviation includes rationale for GxP non-compliance
- 🔄 Benchmark is fully automatable and extensible for future LLMs