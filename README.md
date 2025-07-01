# 🧪 GenAI Recipe Audit Benchmark

A public benchmark framework for evaluating Generative AI models (e.g., OpenAI GPT-4o, Claude, Gemini) on their ability to detect quality issues and GxP-relevant deviations in structured healthcare manufacturing recipes. Designed for reproducibility, model comparison, and long-term auditability.

---

## 🔍 Core Capabilities

- Upload JSON or CSV recipe files  
- Audit entries using multiple GenAI models  
- Detect deviations by ALCOA+ principle  
- Generate detailed PDF audit reports  
- Store JSON logs of all runs for traceability  

---

## 🧠 Key Features

- ✅ Model-agnostic backend (OpenAI, Claude, Gemini, etc.)  
- ✅ Pluggable prompts and evaluation logic per principle  
- ✅ Cross-model performance comparison  
- ✅ Controlled fault injection and synthetic data  
- ✅ Fully timestamped outputs for reproducibility  
- ✅ Cost-aware configuration for scalable execution  

---

## 📂 Project Structure

```
app/           - Streamlit UI frontend
engines/       - Model integration (OpenAI, Gemini, Claude, etc.)
evaluator/     - Evaluation logic per deviation type
pdf/           - PDF generation for reports
test_data/     - Example recipe files with labeled issues
logs/          - JSON logs of each benchmark run
reports/       - Output PDF audit reports
prompts/       - Prompt templates for LLM evaluation
```

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

See the app interface for model selection, entry limits, and PDF download.

---

## 📄 Output Includes

- ✅ Audit summary PDF report:
  - Timestamp (incl. time zone)  
  - File name audited  
  - Models used  
  - Deviation type summary  
  - Compliance metrics  
  - Appendix with full input data  
- ✅ JSON log of the benchmark run with metadata  

---

## ⚖️ License and Reuse

This project is released under the [Apache License 2.0](./LICENSE).

The benchmark is intentionally designed for transparency and reproducibility, but running it at scale may involve substantial API usage costs. While the repository is public, its design and structure are unlikely to support casual reuse without thoughtful adaptation.

If you use or extend this project in a paper, product, or audit system:
- Please credit the original author  
- Link to this repository  
- Clearly document any changes or extensions  

For inquiries, collaboration, or co-authorship, contact information is available via the GitHub or LinkedIn profiles linked in the [README](#).

---

## 💡 Additional Notes

- Entry limits can be adjusted via config or UI  
- Includes clean and 100%-faulty control datasets to test model over/underflagging behavior  
- Prompt templates can be modified for language alignment, site-specific policies, or regulatory emphasis  
- Designed for long-term benchmark automation with minimal manual intervention  

---

© 2025 [AICloudConsulting.com](https://aicloudconsulting.com) — All rights reserved.