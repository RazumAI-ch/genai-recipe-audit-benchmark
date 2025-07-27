-- File: fix_all_sequences.sql
-- Purpose: Automatically reset all sequences to match max(id) per table
--
-- 🛠 Why this is needed:
-- When restoring the database from a backup (e.g., via `make backup-db`),
-- PostgreSQL does not automatically sync sequences (like sample_records_id_seq)
-- to reflect the current data in the table. This can lead to "duplicate key"
-- errors on insert if a sequence is still pointing to an ID that already exists.
--
-- This script loops over all sequences in the database and resets each one
-- to the maximum existing ID in the corresponding table (or 1 if empty).
--
-- 📦 This file is executed automatically during `make backup-db`
-- as part of the `fix-sequences` Makefile target.

DO $$
DECLARE
  r RECORD;
BEGIN
  FOR r IN
    SELECT
      c.relname AS seq_name,
      t.relname AS table_name,
      a.attname AS column_name
    FROM pg_class c
    JOIN pg_depend d ON d.objid = c.oid
    JOIN pg_class t ON d.refobjid = t.oid
    JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = d.refobjsubid
    WHERE c.relkind = 'S'
  LOOP
    EXECUTE format(
      'SELECT setval(%L, COALESCE(MAX(%I), 1)) FROM %I;',
      r.seq_name, r.column_name, r.table_name
    );
  END LOOP;
END$$;