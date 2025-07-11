-- ============================================
-- 📦 LLM Benchmark Schema v1.2 (GxP1 Ready)
-- ============================================

DROP TABLE IF EXISTS
  record_eval_results,
  run_llm_results,
  deviations,
  sample_records,
  deviation_types,
  benchmark_runs,
  llms,
  schema_docs
CASCADE;

-- Registered LLMs
CREATE TABLE llms (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    config_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Benchmark Runs
CREATE TABLE benchmark_runs (
    id SERIAL PRIMARY KEY,
    run_name TEXT,
    sample_size INTEGER,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Deviation Types
CREATE TABLE deviation_types (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    alcoa_principle TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Records
CREATE TABLE sample_records (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES benchmark_runs(id) ON DELETE CASCADE,
    llm_id INTEGER REFERENCES llms(id) ON DELETE CASCADE,
    content JSONB NOT NULL,
    generation_prompt TEXT,
    injected_deviation_ids TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Injected Deviations
CREATE TABLE deviations (
    id SERIAL PRIMARY KEY,
    sample_record_id INTEGER REFERENCES sample_records(id) ON DELETE CASCADE,
    deviation_type_id TEXT REFERENCES deviation_types(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evaluation Results Per Record
CREATE TABLE record_eval_results (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES benchmark_runs(id) ON DELETE CASCADE,
    llm_id INTEGER REFERENCES llms(id) ON DELETE CASCADE,
    sample_record_id INTEGER REFERENCES sample_records(id) ON DELETE CASCADE,
    detected_deviation_ids TEXT[] NOT NULL,
    evaluation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (run_id, llm_id, sample_record_id)
);

-- Run-Level Summary Results
CREATE TABLE run_llm_results (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES benchmark_runs(id) ON DELETE CASCADE,
    llm_id INTEGER REFERENCES llms(id) ON DELETE CASCADE,
    eval_duration_seconds REAL,
    token_input INTEGER,
    token_output INTEGER,
    prompt_price_per_1k NUMERIC(10, 6),
    completion_price_per_1k NUMERIC(10, 6),
    infra_price_per_hour NUMERIC(10, 4),
    cost_source TEXT,
    estimated_cost_usd NUMERIC(10, 4),
    gxp1_score REAL,
    gxp2_score REAL,
    gxp3_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Schema Documentation (optional)
CREATE TABLE schema_docs (
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (table_name, column_name)
);

-- --------------------------------------------
-- Inserts: schema_docs (Full Coverage)
-- --------------------------------------------
INSERT INTO schema_docs (table_name, column_name, description) VALUES

-- llms
('llms', 'id', 'Primary key of the LLM registry.'),
('llms', 'name', 'Display name of the LLM (e.g., "GPT-4o").'),
('llms', 'provider', 'LLM provider (e.g., "openai", "google").'),
('llms', 'model', 'Model version or identifier (e.g., "gpt-4o").'),
('llms', 'config_name', 'Optional label for configuration or environment (e.g., ".env.openai").'),
('llms', 'created_at', 'Timestamp when the LLM was registered.'),

-- benchmark_runs
('benchmark_runs', 'id', 'Primary key of the benchmark run.'),
('benchmark_runs', 'run_name', 'Optional label for the benchmark run.'),
('benchmark_runs', 'sample_size', 'Number of records in this run.'),
('benchmark_runs', 'run_timestamp', 'Time when the benchmark run was started.'),

-- deviation_types
('deviation_types', 'id', 'Unique ID of the deviation type (e.g., "D001").'),
('deviation_types', 'type', 'Technical label of the deviation (e.g., "timestamp_overlap").'),
('deviation_types', 'alcoa_principle', 'GxP ALCOA+ principle violated (e.g., "Accurate").'),
('deviation_types', 'description', 'Human-readable explanation of the deviation type.'),
('deviation_types', 'severity', 'Optional severity level (e.g., "critical", "minor").'),
('deviation_types', 'created_at', 'Timestamp when deviation type was registered.'),

-- sample_records
('sample_records', 'id', 'Primary key of the generated sample record.'),
('sample_records', 'run_id', 'ID of the benchmark run that produced this record.'),
('sample_records', 'llm_id', 'ID of the LLM that generated this sample.'),
('sample_records', 'content', 'JSON structure of the sample (e.g., simulated recipe step).'),
('sample_records', 'generation_prompt', 'Prompt used to generate this record.'),
('sample_records', 'injected_deviation_ids', 'Precomputed list of deviation IDs injected into this record.'),
('sample_records', 'created_at', 'Timestamp when the sample was created.'),

-- deviations
('deviations', 'id', 'Primary key of the injected deviation.'),
('deviations', 'sample_record_id', 'Record that this deviation was injected into.'),
('deviations', 'deviation_type_id', 'ID of the deviation type (e.g., "D003").'),
('deviations', 'created_at', 'Timestamp when the deviation was injected.'),

-- record_eval_results
('record_eval_results', 'id', 'Primary key of the record-level evaluation result.'),
('record_eval_results', 'run_id', 'Benchmark run this evaluation is part of.'),
('record_eval_results', 'llm_id', 'LLM used to evaluate the sample.'),
('record_eval_results', 'sample_record_id', 'ID of the record being evaluated.'),
('record_eval_results', 'detected_deviation_ids', 'List of deviation type IDs detected by the LLM.'),
('record_eval_results', 'evaluation_time', 'When this evaluation was completed.'),

-- run_llm_results
('run_llm_results', 'id', 'Primary key of the run-level summary result.'),
('run_llm_results', 'run_id', 'Benchmark run being evaluated.'),
('run_llm_results', 'llm_id', 'LLM that performed the evaluation.'),
('run_llm_results', 'eval_duration_seconds', 'Total evaluation time in seconds.'),
('run_llm_results', 'token_input', 'Number of input tokens used across all records.'),
('run_llm_results', 'token_output', 'Number of output tokens generated.'),
('run_llm_results', 'prompt_price_per_1k', 'USD cost per 1,000 input tokens.'),
('run_llm_results', 'completion_price_per_1k', 'USD cost per 1,000 output tokens.'),
('run_llm_results', 'infra_price_per_hour', 'Estimated GPU cost per hour (for open models).'),
('run_llm_results', 'cost_source', 'Source of pricing data (e.g., "openai_api").'),
('run_llm_results', 'estimated_cost_usd', 'Estimated total cost of this evaluation.'),
('run_llm_results', 'gxp1_score', 'GxP1 ALCOA+ compliance score (0–1).'),
('run_llm_results', 'gxp2_score', 'Future: structured recipe consistency score.'),
('run_llm_results', 'gxp3_score', 'Future: full trace execution score.'),
('run_llm_results', 'created_at', 'Timestamp when this summary was recorded.');

INSERT INTO llms (name, provider, model, config_name) VALUES
  ('OpenAI GPT-4o',           'openai',  'gpt-4o',           '.env.openai'),
  ('Claude 3 Opus',           'anthropic', 'claude-3-opus', '.env.bedrock'),
  ('Gemini 1.5 Pro',          'google',  'gemini-1.5-pro',   '.env.gemini'),
  ('Grok-1',                  'xai',     'grok-1',           '.env.grok'),
  ('LLaMA 3 65B',             'meta',    'llama3-65b',       '.env.llama'),
  ('Mixtral 8x7B',            'mistral', 'mixtral-8x7b',     '.env.mistral'),
  ('Yi-34B',                  '01-ai',   'yi-34b',           '.env.yi'),
  ('Gemma 27B',               'google',  'gemma-27b',        '.env.gemma'),
  ('Mistral 7B',              'mistral', 'mistral-7b',       '.env.mistral'),
  ('LLaMA 3 8B',              'meta',    'llama3-8b',        '.env.llama');