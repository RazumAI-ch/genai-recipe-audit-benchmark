-- File: db/refresh_schema_docs.sql
-- Purpose: Ensure all columns in the public schema are documented in schema_docs.
--
-- This script is automatically run via the Makefile every time the database
-- is restored from backup and the schema is extracted.
--
-- It inserts entries for any new columns missing from schema_docs,
-- using default descriptions or placeholders.
--
-- At the end, it outputs a list of columns still missing descriptions,
-- so they can be manually completed as needed.

INSERT INTO schema_docs (table_name, column_name, description)
SELECT
    c.table_name,
    c.column_name,
    CASE
        WHEN c.column_name = 'id' THEN 'Primary key for the table.'
        WHEN c.column_name = 'created_at' THEN 'Timestamp when the row was created.'
        WHEN c.column_name = 'updated_at' THEN 'Timestamp when the row was last updated.'
        WHEN c.column_name = 'is_active' THEN 'Flag indicating whether the row is currently active.'
        WHEN c.column_name = 'model' THEN 'Machine-readable model identifier (e.g., gpt-4o, llama3-8b).'
        WHEN c.column_name = 'name' THEN 'Human-readable display name of the model.'
        WHEN c.column_name IN ('method', 'training_method') THEN 'How the model was trained (e.g., lora, full, n/a).'
        WHEN c.column_name = 'model_path' THEN 'Filesystem or cloud path to the model artifact.'
        WHEN c.column_name = 'provider' THEN 'Which vendor or organization provides the model.'
        WHEN c.column_name LIKE '%llm_id' THEN 'Reference to the LLM used in this record.'
        WHEN c.column_name LIKE '%run_id' THEN 'Reference to the benchmark run.'
        WHEN c.column_name LIKE '%sample_record_id' THEN 'Reference to a generated sample record.'
        WHEN c.column_name LIKE '%deviation_type_id' THEN 'Reference to a known deviation type.'
        ELSE '[TODO: Add description]'
    END
FROM information_schema.columns c
WHERE c.table_schema = 'public'
  AND NOT EXISTS (
    SELECT 1 FROM schema_docs d
    WHERE d.table_name = c.table_name
      AND d.column_name = c.column_name
)
ORDER BY c.table_name, c.ordinal_position;

-- Show all columns that still need descriptions
SELECT table_name, column_name
FROM schema_docs
WHERE description LIKE '[TODO:%]'
ORDER BY table_name, column_name;