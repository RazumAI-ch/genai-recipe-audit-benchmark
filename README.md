# GenAI Recipe Audit Benchmark

Benchmark for evaluating how well large language models detect, classify, and explain GxP-relevant deviations in pharmaceutical manufacturing recipes.

Focus Areas:

* GxP1 – ALCOA+ deviation detection & classification (implemented)
* GxP2 – Recipe logic consistency deviation detection & classification (future)
* GxP3 – Execution trace deviation detection & classification (future)

Config & scoring rules: [`docs/CONFIG.md`](docs/CONFIG.md) (aligned with [`config/models.yaml`](config/models.yaml)).

---

## Deployment (Remote or Local)

```bash
# Generate dedicated SSH key (once, skip for local install)
ssh-keygen -t ed25519 -f ~/.ssh/genai-benchmark -C "genai-benchmark"
# Upload ~/.ssh/genai-benchmark.pub to your cloud provider during instance creation

# SSH into server (skip for local install)
ssh -i ~/.ssh/genai-benchmark your-username@your-server-ip

# Clone repository
git clone https://github.com/rasm-ai/genai-recipe-audit-benchmark.git
cd genai-recipe-audit-benchmark

# Copy preconfigured .env from local to server (skip for local install)
scp -i ~/.ssh/genai-benchmark /path/to/local/.env your-username@your-server-ip:/home/your-username/genai-recipe-audit-benchmark/.env
# For local install: cp .env.example .env && nano .env

# Deploy (installs Docker if missing)
make deploy-remote

# Run quick test
make run
```

---

License: see [LICENSE](LICENSE)
