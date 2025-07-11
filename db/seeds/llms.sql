-- ============================================
-- File: db/seeds/llms.sql
-- Purpose: Initial set of LLMs to be covered by the benchmark
-- Usage: Run manually or via `make setup-db` or `make load-llms`
-- ============================================

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

