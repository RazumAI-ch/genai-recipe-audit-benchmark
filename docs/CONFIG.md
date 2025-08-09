# File: docs/CONFIG.md

# CONFIG.md – Configuration Specification (Agreement Version)

## Scope

This document defines the **agreement/spec** that governs how LLM model configs are structured, interpreted, and evaluated in this repository, including full benchmark scoring logic.

* **Authoritative data file:** `config/models.yaml`
* **Authoritative version field:** `config/models.yaml:version`
* **This document mirrors that version** and contains all rules, policies, and logic required to implement or interpret the benchmark.

---

## Agreement vs. Application Version

* **Agreement/Spec version** (this document + `models.yaml:version`): the contract for fields, merge rules, scoring rules, and repo-wide policies.
* **Application/release version**: the overall software version of the benchmark system (tracked separately, e.g., Git tags). It is **independent** from the agreement/spec version.

---

## Spec Versioning

**Current spec version:** `0.2.0`
**Canonical source:** the `version` field in `config/models.yaml`.
This CONFIG.md must **match** that value.

### What the spec version covers

1. The structure and fields of `config/models.yaml`
2. The merge/precedence semantics defined here
3. Benchmark scoring logic
4. Repository-wide rules affecting config interpretation

### When to bump

* **MAJOR (X.0.0)** – Backward-incompatible changes to schema or scoring logic
* **MINOR (0.X.0)** – Backward-compatible updates, new optional fields, or scoring adjustments
* **PATCH (0.1.X)** – Clarifications/typos that don’t alter behavior

Any change to scoring methodology or evaluation logic must trigger a spec version bump.

### Validation rule

CI/loader must check:
`config/models.yaml:version == docs/CONFIG.md:Current spec version`
If mismatch → fail CI or emit an error.

---

## Action and Dependency Markers

All conditional actions must use:

```
ACTION:<ACTION_NAME>; REF=config/models.yaml:version; WHEN:<comparison><semver>; NOTE:<free text>
```

Example:

```python
LLM_TEMPERATURE = 0.0  # ACTION:REMOVE_AFTER; REF=config/models.yaml:version; WHEN:>=1.0.0; NOTE: Use global_model_defaults.temperature from YAML
```

---

## File naming and extensions

* Use `.yaml` across the repository (not `.yml`).
* Canonical config path: `config/models.yaml`.

---

## Merge Precedence

Lowest → highest:

1. `global_model_defaults`
2. `provider_defaults[provider]`
3. `models[MODEL_KEY]`

No default provider — each model must explicitly set `provider`.

---

## Required Fields per Model

* `provider` — must match `provider_defaults`
* `model_id` — canonical model identifier (provider-neutral format; provider maps internally)

Optional overrides:

* `temperature`
* `max_tokens`
* `batch_size`
* `enabled`

---

## Provider-specific rules for `model_id`

* **OPENAI**: OpenAI public model name (`gpt-4o`)
* **VERTEX\_AI**: Vertex model name (`gemini-1.5-pro`)
* **VULTR**: Canonical neutral model name (`Mistral-7B-Instruct-v0.3`); provider maps internally to API-specific name

---

## Access Method Policy

No config field for API vs. deployment — provider implementation decides. This keeps `models.yaml` provider-agnostic and allows execution method changes without altering configuration. Execution method is logged for informational purposes but not used for ranking.

---

## Scoring Logic – GxP1

GxP1 scoring evaluates a model’s ability to **detect and classify** ALCOA+ deviations.

### Penalty Rules

* **Correct detection, correct severity:** No penalty
* **Correct detection, incorrect severity:** Penalty = difference in severity weight
* **Missed deviation:** Penalty = full severity weight
* **Hallucinated deviation:** Penalty = predicted severity weight

### Severity Weights

* Minor: 1
* Medium: 10
* Critical: 100

### Final Score Calculation

```
GxP1_Score = 1.0 − (P_model / P_worst)
```

Where:

* `P_model` = total penalty for the evaluated model
* `P_worst` = highest penalty among all models in the run

Score range:

* **1.0** → perfect detection & classification
* **0.0** → worst model in the run

### Worked Example

1. Record contains one Medium deviation (weight 10)
2. Model flags it as Minor (weight 1) → penalty = |10 - 1| = 9
3. Model misses another Critical deviation (weight 100) → penalty = 100
4. Model hallucinates a Medium deviation → penalty = 10
5. `P_model` = 9 + 100 + 10 = 119
6. If `P_worst` = 238, then:

```
GxP1_Score = 1.0 - (119 / 238) = 1.0 - 0.5 = 0.5
```

---

## Implied Connections

For API providers, the environment must contain `{PROVIDER_KEY}_API_KEY`.

---

## Example Configuration

```yaml
# File: config/models.yaml
version: "0.1.0"  # UNIQUE_ID: config/models.yaml:version

global_model_defaults:
  temperature: 0.0
  max_tokens: 2048
  enabled: true

provider_defaults:
  OPENAI:
    batch_size: 20
  VERTEX_AI:
    batch_size: 10
  VULTR:
    batch_size: 50

models:
  EVALUATED_LLM_OPENAI_GPT_4O:
    provider: OPENAI
    model_id: "gpt-4o"

  EVALUATED_LLM_MISTRAL_7B_INSTRUCT:
    provider: VULTR
    model_id: "Mistral-7B-Instruct-v0.3"
    max_tokens: 1536
```

---

## Deprecations and migration to YAML-only

* Python-side registry constants and static enable/disable sets are being removed.
* The single source of truth for model availability, identifiers, and scoring rules is `config/models.yaml` + `docs/CONFIG.md`.
* All deferred or conditional changes must use the `ACTION:` marker format.
