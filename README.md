# GenAI Recipe Audit Benchmark

A reproducible benchmark for evaluating how well large language models detect, classify, and explain GxP-relevant deviations in pharmaceutical manufacturing recipes. Designed for regulatory-grade infrastructure auditing with closed, open, and self-trained proprietary models.

**Focus Areas**

* GxP1 – ALCOA+ deviation detection & classification (implemented)
* GxP2 – Recipe logic consistency deviation detection & classification (future)
* GxP3 – Execution trace deviation detection & classification (future)

Config & scoring rules: [`docs/CONFIG.md`](docs/CONFIG.md) (aligned with [`config/models.yaml`](config/models.yaml)).

---

## Remote Deployment (Ubuntu/Debian)

```bash
# SSH into your server
ssh -i /path/to/key.pem user@your.server.ip

# Install Docker & Docker Compose
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
docker --version && docker compose version
sudo usermod -aG docker $USER && newgrp docker

# Clone the repository
git clone https://github.com/rasm-ai/genai-recipe-audit-benchmark.git
cd genai-recipe-audit-benchmark

# Configure environment variables
cp .env.example .env
nano .env  # Add API keys

# Deploy and run examples
make deploy-remote
make run        # Quick test (1 record)
make run 50     # Medium test (50 records)
make run-full   # Full benchmark (10,000 records)
```

---

## Local Deployment (Docker already installed)

```bash
# Clone the repository
git clone https://github.com/rasm-ai/genai-recipe-audit-benchmark.git
cd genai-recipe-audit-benchmark

# Configure environment variables
cp .env.example .env
nano .env  # Add API keys

# Start and run
docker compose up -d
make run
```

---

**License**
See [LICENSE](LICENSE) file in the repository root.
