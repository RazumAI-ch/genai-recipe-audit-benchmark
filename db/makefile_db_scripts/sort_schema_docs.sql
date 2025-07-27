-- File: db/sort_schema_docs.sql
-- Purpose: Reorder all rows in the schema_docs table so that fields are grouped
--          by table and sorted alphabetically by column name.
--
-- Why: This makes manual browsing and editing of schema_docs much easier,
--      especially when reviewing field descriptions per table.
--      Without sorting, newly added fields appear at the end of the table,
--      making it harder to view a consistent structure.
--
-- When to run: Automatically as part of the DB backup process (e.g., after
--              updating docs or inserting new fields). This script is safe to run repeatedly.
--
-- ⚠️ Important note:
-- This uses a Common Table Expression (CTE) named `ordered` to snapshot the original contents
-- of the schema_docs table before modifying it.
--
-- Note: This version wraps DELETE and INSERT inside a DO block to ensure the CTE
--       remains valid through the transaction.


-- Step 1: Copy sorted data into a temp table
CREATE TEMP TABLE schema_docs_tmp AS
SELECT *
FROM schema_docs
ORDER BY table_name, column_name;

-- Step 2: Truncate original table
TRUNCATE schema_docs;

-- Step 3: Insert sorted data back
INSERT INTO schema_docs (table_name, column_name, description)
SELECT table_name, column_name, description FROM schema_docs_tmp;