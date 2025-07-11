-- ============================================
-- File: db/seeds/deviation_types.sql
-- Purpose: Master list of deviation types used in benchmark injection and scoring
-- Scope: Covers all ALCOA+ principles (Accurate, Attributable, etc.)
-- Usage: Run manually or via `make load-deviation-types`
-- ============================================

-- ============================================
-- Seed: Deviation Types for ALCOA+ (v1.0)
-- ============================================

INSERT INTO deviation_types (id, type, alcoa_principle, description, severity) VALUES
-- ACCURATE
('D001', 'timestamp_overlap',        'Accurate',        'Two steps share the same timestamp', 'major'),
('D002', 'missing_unit',             'Accurate',        'Quantity is provided without a unit of measure', 'minor'),
('D003', 'incorrect_calculation',    'Accurate',        'Derived value or conversion is incorrect', 'major'),
('D004', 'mislabeling',              'Accurate',        'Material or product label does not match data entry', 'critical'),

-- ATTRIBUTABLE
('D005', 'missing_actor',            'Attributable',    'No person or system recorded the step', 'critical'),
('D006', 'ambiguous_user',           'Attributable',    'Initials or ID are unclear or non-unique', 'major'),
('D007', 'unlinked_signature',       'Attributable',    'Signature exists but not linked to user metadata', 'major'),

-- CONTEMPORANEOUS
('D008', 'future_date',              'Contemporaneous', 'Action recorded as occurring in the future', 'major'),
('D009', 'backdated_entry',          'Contemporaneous', 'Timestamp manually changed to appear earlier', 'major'),
('D010', 'delayed_entry',            'Contemporaneous', 'Record entered significantly after event without explanation', 'major'),

-- ORIGINAL
('D011', 'field_overwritten',        'Original',        'A previously recorded value was overwritten', 'major'),
('D012', 'duplicate_entry',          'Original',        'Two identical entries exist for the same step', 'minor'),
('D013', 'altered_timestamp',        'Original',        'Timestamp altered after initial logging', 'critical'),
('D014', 'fake_signature',           'Original',        'Operator name not found in authorization list', 'critical'),
('D015', 'external_copy_paste',      'Original',        'Text copy-pasted from external document or clipboard', 'minor'),

-- LEGIBLE
('D016', 'unclear_instruction',      'Legible',         'Instruction is vague or ambiguous', 'minor'),
('D017', 'inconsistent_formatting',  'Legible',         'Inconsistent use of units, symbols, or decimals', 'minor'),
('D018', 'handwriting_simulation',   'Legible',         'Text includes simulated handwriting font', 'minor'),
('D019', 'placeholder_value',        'Legible',         'Placeholder like "TBD" or "123" left in final record', 'minor'),

-- COMPLETE
('D020', 'missing_field',            'Complete',        'Required field is blank or NULL', 'major'),
('D021', 'partial_data',             'Complete',        'Only partial value is recorded (e.g., only time, no date)', 'major'),
('D022', 'step_skipped',             'Complete',        'Entire procedural step is missing', 'critical'),

-- CONSISTENT
('D023', 'step_out_of_order',        'Consistent',      'Process step occurs out of defined sequence', 'critical'),
('D024', 'status_mismatch',          'Consistent',      'Status field conflicts with actual completion state', 'major'),
('D025', 'conflicting_approvals',    'Consistent',      'Two conflicting sign-offs recorded for the same step', 'critical'),

-- ENDURING
('D026', 'non_auditable_change',     'Enduring',        'Change made without audit trail/log', 'critical'),
('D027', 'missing_change_log',       'Enduring',        'No record of changes to a previously edited field', 'major'),

-- RETRIEVABLE
('D028', 'orphan_reference',         'Retrievable',     'Reference made to a record that doesn’t exist or can’t be found', 'major'),
('D029', 'broken_link',              'Retrievable',     'URL or internal reference is no longer valid', 'minor'),
('D030', 'archival_failure',         'Retrievable',     'Record flagged as archived but not accessible on demand', 'critical');