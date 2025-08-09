CONFIG.md – Configuration Specification (Agreement Version)

Scope
This document defines the agreement/spec governing how the GenAI Recipe Audit Benchmark is structured, configured, and evaluated, including benchmark scoring logic, architecture, and future evaluation tracks.

* Authoritative data file: config/models.yaml
* Authoritative version field: config/models.yaml\:version
* This document mirrors that version and contains all rules, policies, and logic required to implement or interpret the benchmark.

Agreement vs. Application Version

* Agreement/Spec version (this document + models.yaml\:version): the contract for fields, merge rules, scoring rules, architecture, and repo-wide policies.
* Application/release version: the overall software version of the benchmark system (tracked separately, e.g., Git tags). Independent from the agreement/spec version.

Spec Versioning
Current spec version: 0.2.0
Canonical source: version field in config/models.yaml.

Covers:

1. config/models.yaml schema and merge rules
2. Scoring logic
3. System architecture layers
4. Future track definitions (GxP2, GxP3)
5. Repository-wide policies

When to bump:

* MAJOR (X.0.0) – Breaking changes to schema or scoring logic
* MINOR (0.X.0) – Backward-compatible schema/policy updates or new optional fields/tracks
* PATCH (0.1.X) – Clarifications or typos

Merge Precedence

1. global\_model\_defaults
2. provider\_defaults\[provider]
3. models\[MODEL\_KEY]

No default provider — every model must explicitly set provider.

Required Fields per Model

* provider — must match provider\_defaults
* model — canonical model identifier (provider-neutral; provider maps internally)

Optional overrides:

* temperature
* max\_tokens
* batch\_size
* enabled

Model Key Naming Convention
All keys under models: must follow the format:
EVALUATED\_LLM\_\<MODEL\_NAME>
Where \<MODEL\_NAME> is the canonical model name in uppercase, with hyphens replaced by underscores.

Provider-specific Rules for model

* OPENAI: OpenAI public model name (gpt-4o)
* VERTEX\_AI: Vertex model name (gemini-1.5-pro)
* VULTR: Canonical neutral model name (Mistral-7B-Instruct-v0.3); provider maps internally to API-specific string.

Capitalization Rule
Capitalization in model IDs must match canonical provider-neutral names exactly.

Access Method Policy
No config field for API vs. deployment — provider implementation decides. Keeps models.yaml provider-agnostic; allows execution method changes without altering config. Execution method is logged but not used in ranking.

Scoring Logic – GxP1
GxP1 evaluates model ability to detect and classify GxP-relevant deviations in structured recipe records according to ALCOA+ principles:

* Attributable, Legible, Contemporaneous, Original, Accurate, Complete, Consistent, Enduring, Available.

Penalty Rules:

* Correct detection, correct severity: No penalty
* Correct detection, incorrect severity: Penalty = difference in severity weight
* Missed deviation: Penalty = full severity weight
* Hallucinated deviation: Penalty = predicted severity weight

Severity Weights:

* Minor: 1
* Medium: 10
* Critical: 100

Formula:
GxP1\_Score = 1.0 − (P\_model / P\_worst)
Where:

* P\_model = total penalty for the model
* P\_worst = highest penalty in the run

Score range:

* 1.0 → perfect detection and classification
* 0.0 → worst performance in the run

Example:

* Medium deviation flagged as Minor → penalty = |10 − 1| = 9
* Critical deviation missed → penalty = 100
* Medium deviation hallucinated → penalty = 10
* P\_model = 119, P\_worst = 238 → score = 1 − (119/238) = 0.5

System Architecture Overview
The benchmark system is modular and containerized for reproducibility, traceability, and maintainability.
Layers:

1. PostgreSQL Database – Stores sample records, deviations, configs, results, and metadata with referential integrity and version tracking.
2. Model Integration Layer – Common wrapper for proprietary and open models, handling auth, prompts, batching, parsing.
3. Prompt Configuration & Evaluation Logic – Central YAML prompt definitions; parses model outputs; computes scores.
4. Deviation Injection Engine – Generates synthetic deviations in clean records with full metadata.
5. Benchmark Runner – Orchestrates dataset load, model execution, logging, result storage.
6. Training Module – Supports LoRA and full fine-tuning on synthetic GxP data; logs tokens, loss, duration; outputs adapters.
7. Output & Reporting Engine – Produces JSON summaries, logs, and archives; future PDF/dashboards.

Provider Runtime Configs

* Location: config/providers/{PROVIDER}.yaml
* Purpose: Store provider-specific operational settings and endpoint mappings.
* Allowed keys:

  * api\_key\_env
  * base\_url
  * http.timeout\_seconds
  * http.max\_retries
  * http.rate\_limit\_sleep
  * model\_overrides\[model].endpoint\_model\_id
* Forbidden keys (must never appear in provider files — only in models.yaml or defaults):

  * temperature
  * max\_tokens
  * batch\_size
  * enabled
  * model
* Validation rule: Loader must error if a provider file contains any forbidden key.
* Merge precedence: Provider file values are merged after provider\_defaults but may not override any value explicitly set in models.yaml.

Future Tracks
GxP2 – Recipe Logic Consistency Analysis

* Evaluates violations of recipe logic across records (e.g., step order, durations, missing phases).
* Tests multi-step reasoning and context beyond isolated records.

GxP3 – Execution Log Deviation Detection

* Evaluates execution-time anomalies in logs (e.g., operator mismatch, unexpected step re-entry, delays).
* Targets temporal and behavioral trace validation.

Implied Connections
For API providers, the environment must contain {PROVIDER\_KEY}\_API\_KEY.

Deprecations
Python-side constants and static enable/disable sets are being removed. Single source of truth for model availability, identifiers, and scoring rules is config/models.yaml + docs/CONFIG.md.

Formatting Policy
All formatting must be minimalistic and consistent across updates.
