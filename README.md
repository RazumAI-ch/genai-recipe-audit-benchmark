# 🧪 GenAI Recipe Audit Benchmark

A benchmark to evaluate how well Generative AI models (e.g. GPT-4o, Claude, Gemini, Mistral, LLaMA, etc.) are able to identify and classify ALCOA+ deviations.

A **diverse mix of models** are evaluated including:
- Proprietary closed-source LLMs (e.g., OpenAI GPT-4o, Gemini, Claude)
- Open-source foundation models (e.g., Mistral, LLaMA)
- **Our own LoRA-trained variants** fine-tuned on structured GxP data

---

## 📊 GxP Scoring

| Score     | Scope                     | Availability  |
|-----------|---------------------------|---------------|
| **GxP1**  | ALCOA+ violation detection | ✅ Open source |
| **GxP2**  | Recipe logic consistency   | 🔒 Commercial  |
| **GxP3**  | Execution trace validation | 🔒 Commercial  |

GxP1 detects timestamp issues, missing operators, overwritten fields, etc., with per-model scores normalized to [0–1].

---

## 🔧 Capabilities

- Generate structured samples with injected deviations  
- Evaluate across OpenAI, Claude, Gemini, Mistral, etc.  
- Benchmark open models — including our own **LoRA-trained fine-tunes**  
- Compare quality, speed, and price across LLMs  
- Fully reproducible via Docker + PostgreSQL + Makefile  

---

## 📂 Project Structure

```
genai-recipe-audit-benchmark/
├── db/            # PostgreSQL schema + seed data
├── scripts/       # Training data generation and LoRA export
├── models/        # LoRA adapters and full fine-tuned models
├── benchmark/     # Core scoring logic and run orchestration
├── config/        # Prompt templates and pricing info
├── llms/          # LLM wrappers (OpenAI, Gemini, etc.)
├── docs/          # CLI usage and GxP methodology
└── main.py        # Benchmark entry point
```

---

## 🚀 Run Locally

```bash
docker-compose up -d
make setup-db
python main.py
```

This runs a benchmark across all configured models, stores results, and outputs per-model cost + GxP1 scores.

---

## 💼 Commercial Extensions

GxP2 and GxP3 are available via AICloudConsulting as part of a benchmark pilot for regulated clients.  
Use them to evaluate model alignment with real-world recipes and execution logs.

👉 [AICloudConsulting.com](https://aicloudconsulting.com)

---

© 2025 AICloudConsulting — All rights reserved.