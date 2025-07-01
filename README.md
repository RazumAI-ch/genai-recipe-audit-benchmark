# GenAI Recipe Audit Benchmark

A private benchmark framework for evaluating Generative AI models (e.g., OpenAI GPT-4o, Claude, Gemini) on their ability to identify deviations and quality issues in healthcare manufacturing recipes. Designed to support GxP-relevant use cases with cross-model comparison, audit trail logging, and long-term reproducibility.

## 🔍 Core Capabilities
- Upload JSON or CSV recipe files
- Audit entries using multiple GenAI models
- Evaluate deviation detection accuracy
- Generate detailed PDF audit reports
- Log all interactions with timestamped metadata

## 🧠 Key Features
- Model-agnostic architecture (OpenAI, Claude, Gemini, etc.)
- Prompt-based deviation checks
- Pluggable evaluation logic per ALCOA+ principle
- Cross-model performance comparison
- Controlled data injection and PDF generation

## 🧱 Project Structure
```
app/           - Streamlit front-end
engines/       - Model-specific wrappers (e.g., OpenAI, Gemini)
evaluator/     - Evaluation and comparison logic
pdf/           - PDF audit report generator
test_data/     - Realistic sample recipes (with known issues)
logs/          - JSON logs of each benchmark run
reports/       - Output audit PDFs
prompts/       - Structured prompt templates
```

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run app/main.py
```

## 📝 Output Files
- PDF report including:
  - Timestamp with time zone
  - Audited file name
  - Model versions used
  - Deviation summary table
  - Full input appendix
- JSON log per run for reproducibility and traceability

## 🔐 Project Status
This repository is **private**. It contains full implementation logic, test data, prompt structure, and evaluation methodology that may be published selectively in the future. 

If you are reviewing this as a collaborator, co-author, or advisor, please treat contents as confidential unless otherwise agreed.

## 📌 Notes
- Only the first N entries may be tested per run (configurable)
- All test cases include both realistic and edge-case deviations
- Output folder names are timestamped to support long-term comparisons
- Includes control datasets (clean and 100% faulty) for model over/underflagging analysis

---

© 2025 AICloudConsulting.com — All rights reserved.
