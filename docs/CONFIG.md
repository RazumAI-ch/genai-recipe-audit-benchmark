# CONFIG.md – Configuration Specification (Agreement Version)

## 1. Scope
Defines the agreement/spec for the GenAI Recipe Audit Benchmark, covering configuration, scoring logic, architecture, and repository-wide policies.

- **Authoritative file:** `config/models.yaml`
- **Version field:** `config/models.yaml:version`
- This doc mirrors that version.

---

## 2. Agreement vs. Application Version
- **Agreement/Spec version** = This doc + `models.yaml:version`
- **Application/release version** = Software version (e.g., Git tags)

---

## 3. Spec Versioning
- **Current:** `0.2.1` (see `config/models.yaml`)
- **MAJOR** X.0.0 – Breaking changes
- **MINOR** 0.X.0 – Backward-compatible schema/policy updates
- **PATCH** 0.1.X – Clarifications or typos

---

## 4. Merge Precedence
1. `global_model_defaults`
2. `provider_defaults[provider]`
3. `models[MODEL_KEY]`

---

## 5. Required Fields per Model
- `provider` — must match a `provider_defaults` key
- `model` — canonical model identifier (provider-neutral)

**Optional overrides:**
- `temperature`
- `max_tokens`
- `batch_size`
- `enabled`

---

## 6. Model Key Naming Convention
`EVALUATED_LLM_<MODEL_NAME>`  
`<MODEL_NAME>` in uppercase, hyphens → underscores.

---

## 7. Provider Rules for `model`
- **OPENAI:** Public model name (e.g., `gpt-4o`)
- **GEMINI_STUDIO / VERTEX_AI:** Vertex/Gemini name (e.g., `gemini-1.5-pro`)
- **VULTR:** Canonical neutral name (e.g., `Mistral-7B-Instruct-v0.3`)

---

## 8. Capitalization Rule
Model IDs in YAML must match canonical provider-neutral names exactly.

---

## 9. Access Method Policy
No `api` vs. `deployment` field — provider implementation decides.

---

## 10. HTTP Defaults
HTTP-level defaults may be defined under `provider_defaults`.  
Providers can override per-provider.

Keys:
- `http.timeout_seconds`
- `http.max_retries`
- `http.rate_limit_sleep`

---

## 11. Scoring Logic – GxP1
Evaluates detection & classification of GxP deviations (ALCOA+).

**Penalty rules:**
- Correct detection + correct severity → No penalty
- Correct detection + wrong severity → Penalty = diff in severity weight
- Missed deviation → Full severity weight
- Hallucinated deviation → Predicted severity weight

**Severity weights:**
- Minor = 1
- Medium = 10
- Critical = 100

**Formula:**
```
GxP1_Score = 1.0 − (P_model / P_worst)
```

---

## 12. System Architecture
1. PostgreSQL DB – Stores all data & configs
2. Model Integration Layer – Wrappers for models
3. Prompt Config & Evaluation Logic – Central YAML
4. Deviation Injection Engine – Creates synthetic deviations
5. Benchmark Runner – Orchestrates runs
6. Training Module – LoRA/full fine-tuning
7. Output & Reporting – JSON, logs, future dashboards

---

## 13. Provider Runtime Configs
- Location: `config/providers/{PROVIDER}.yaml`
- Purpose: Provider-specific operational settings
- Allowed keys:
  - `api_key_env`
  - `base_url`
  - `http.timeout_seconds`
  - `http.max_retries`
  - `http.rate_limit_sleep`
  - `model_overrides[model].endpoint_model_id`
- Forbidden keys:
  - `temperature`
  - `max_tokens`
  - `batch_size`
  - `enabled`
  - `model`

---

## 14. Future Tracks
- **GxP2** – Recipe logic consistency
- **GxP3** – Execution log deviation detection

---

## 15. Implied Connections
For API providers: env var must be `{PROVIDER_KEY}_API_KEY`.

---

## 16. Deprecations
Static enable/disable sets & Python-side constants removed.  
Single source: `config/models.yaml` + `CONFIG.md`.

---

## 17. Formatting Policy
Minimalistic, consistent, no decorative formatting.