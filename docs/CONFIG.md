File: docs/CONFIG.md

CONFIG.md – Configuration Specification (Agreement Version)

Scope

This document defines the agreement/spec governing how the GenAI Recipe Audit Benchmark is structured, configured, and evaluated, including benchmark scoring logic, architecture, and future evaluation tracks.
	•	Authoritative data file: config/models.yaml
	•	Authoritative version field: config/models.yaml:version
	•	This document mirrors that version and contains all rules, policies, and logic required to implement or interpret the benchmark.

⸻

Agreement vs. Application Version
	•	Agreement/Spec version (this document + models.yaml:version): the contract for fields, merge rules, scoring rules, architecture, and repo-wide policies.
	•	Application/release version: the overall software version of the benchmark system (tracked separately, e.g., Git tags). Independent from the agreement/spec version.

⸻

Spec Versioning

Current spec version: 0.1.0
Canonical source: version field in config/models.yaml.

Covers:
	1.	config/models.yaml schema and merge rules
	2.	Scoring logic
	3.	System architecture layers
	4.	Future track definitions (GxP2, GxP3)
	5.	Repository-wide policies

When to bump:
	•	MAJOR (X.0.0) – Breaking changes to schema or scoring logic
	•	MINOR (0.X.0) – Backward-compatible schema/policy updates or new optional fields/tracks
	•	PATCH (0.1.X) – Clarifications or typos

⸻

Merge Precedence
	1.	global_model_defaults
	2.	provider_defaults[provider]
	3.	models[MODEL_KEY]

No default provider — every model must explicitly set provider.

⸻

Required Fields per Model
	•	provider — must match provider_defaults
	•	model_id — canonical model identifier (provider-neutral; provider maps internally)

Optional overrides:
	•	temperature
	•	max_tokens
	•	batch_size
	•	enabled

⸻

Provider-specific Rules for model_id
	•	OPENAI: OpenAI public model name (gpt-4o)
	•	VERTEX_AI: Vertex model name (gemini-1.5-pro)
	•	VULTR: Canonical neutral model name (Mistral-7B-Instruct-v0.3); provider maps internally to API-specific string.

⸻

Access Method Policy

No config field for API vs. deployment — provider implementation decides. Keeps models.yaml provider-agnostic; allows execution method changes without altering config. Execution method is logged but not used in ranking.

⸻

Scoring Logic – GxP1

GxP1 evaluates model ability to detect and classify GxP-relevant deviations in structured recipe records according to ALCOA+ principles:
	•	Attributable, Legible, Contemporaneous, Original, Accurate, Complete, Consistent, Enduring, Available.

Penalty Rules:
	•	Correct detection, correct severity: No penalty
	•	Correct detection, incorrect severity: Penalty = difference in severity weight
	•	Missed deviation: Penalty = full severity weight
	•	Hallucinated deviation: Penalty = predicted severity weight

Severity Weights:
	•	Minor: 1
	•	Medium: 10
	•	Critical: 100

Formula:

GxP1_Score = 1.0 − (P_model / P_worst)

Where:
	•	P_model = total penalty for the model
	•	P_worst = highest penalty in the run

Score range:
	•	1.0 → perfect detection and classification
	•	0.0 → worst performance in the run

Example:
	•	Medium deviation flagged as Minor → penalty = |10 − 1| = 9
	•	Critical deviation missed → penalty = 100
	•	Medium deviation hallucinated → penalty = 10
	•	P_model = 119, P_worst = 238 → score = 1 − (119/238) = 0.5

⸻

System Architecture Overview

The benchmark system is modular and containerized for reproducibility, traceability, and maintainability.

Layers:
	1.	PostgreSQL Database – Stores sample records, deviations, configs, results, and metadata with referential integrity and version tracking.
	2.	Model Integration Layer – Common wrapper for proprietary and open models, handling auth, prompts, batching, parsing.
	3.	Prompt Configuration & Evaluation Logic – Central YAML prompt definitions; parses model outputs; computes scores.
	4.	Deviation Injection Engine – Generates synthetic deviations in clean records with full metadata.
	5.	Benchmark Runner – Orchestrates dataset load, model execution, logging, result storage.
	6.	Training Module – Supports LoRA and full fine-tuning on synthetic GxP data; logs tokens, loss, duration; outputs adapters.
	7.	Output & Reporting Engine – Produces JSON summaries, logs, and archives; future PDF/dashboards.

⸻

Future Tracks

GxP2 – Recipe Logic Consistency Analysis
	•	Evaluates violations of recipe logic across records (e.g., step order, durations, missing phases).
	•	Tests multi-step reasoning and context beyond isolated records.

GxP3 – Execution Log Deviation Detection
	•	Evaluates execution-time anomalies in logs (e.g., operator mismatch, unexpected step re-entry, delays).
	•	Targets temporal and behavioral trace validation.

⸻

Implied Connections

For API providers, the environment must contain {PROVIDER_KEY}_API_KEY.

⸻

Example Configuration

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


⸻

Deprecations

Python-side constants and static enable/disable sets are being removed. Single source of truth for model availability, identifiers, and scoring rules is config/models.yaml + docs/CONFIG.md.