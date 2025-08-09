# GenAI Recipe Audit Benchmark

A reproducible benchmark for evaluating how well large language models identify, classify, and explain GxP-relevant deviations in pharmaceutical manufacturing recipes. Designed for regulatory-grade infrastructure auditing with closed, open, and self-trained proprietary models.

Focus areas:
- GxP1: ALCOA+ deviation detection & classification (✅ Open source)
- GxP2: Recipe logic consistency deviation detection & classification (❌ Future)
- GxP3: Execution trace deviation detection & classification (❌ Future)

Dataset is synthetically generated with 2% deviation injection. Detailed scoring rules, severity weights, and normalization formula are in [docs/CONFIG.md](docs/CONFIG.md) to stay synchronized with the config/models.yaml spec version.

We monitor API usage, token cost, runtime per model, and score per run.

## Configuration Details
- **Configuration Specification**: All configuration rules, defaults, and agreements are in [docs/CONFIG.md](docs/CONFIG.md). This is the authoritative spec for config/models.yaml.
- **Scoring Logic**: Complete rules, penalties, and formulas are defined in [docs/CONFIG.md](docs/CONFIG.md).
- **Model Coverage**: See [config/models.yaml](config/models.yaml) for the current list of enabled and disabled models.

## Running & Testing
Run locally:
```bash
docker-compose up -d
python main.py
```
Unit tests: See [docs/CONFIG.md](docs/CONFIG.md) for rules tied to config/models.yaml.

For licensing details, see the LICENSE file in the repository root.