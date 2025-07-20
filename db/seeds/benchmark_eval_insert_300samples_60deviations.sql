-- Insert benchmark run
INSERT INTO benchmark_runs (id, run_name, sample_size, run_timestamp) 
VALUES (1, 'Run_18-Jul-2025', 300, '2025-07-17 23:59:20');

-- Ensure OpenAI GPT-4o exists
INSERT INTO llms (id, name, provider, model, config_name, training_method, model_path, logical_name, model_type, notes)
VALUES (1, 'OpenAI GPT-4o', 'OpenAI', 'gpt-4o', NULL, NULL, NULL, 'gpt-4o', 'api', 'Baseline OpenAI model for benchmark')
ON CONFLICT (id) DO NOTHING;

-- Insert sample records
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (1, 1, 1, '{"step_id": "STP-0001", "actor": "user5", "timestamp": "2025-07-14T15:00:00Z", "equipment": "EQ-822", "quantity": "357 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (2, 1, 1, '{"step_id": "STP-0002", "actor": "user3", "timestamp": "2025-07-12T15:00:00Z", "equipment": "EQ-509", "quantity": "352 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (3, 1, 1, '{"step_id": "STP-0003", "actor": "user4", "timestamp": "2025-07-22T15:00:00Z", "equipment": "EQ-126", "quantity": "135 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (4, 1, 1, '{"step_id": "STP-0004", "actor": "user4", "timestamp": "2025-07-05T09:00:00Z", "equipment": "EQ-587", "quantity": "280 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (5, 1, 1, '{"step_id": "STP-0005", "actor": "user2", "timestamp": "2025-07-20T14:00:00Z", "equipment": "EQ-392", "quantity": "172 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (6, 1, 1, '{"step_id": "STP-0006", "actor": "user4", "timestamp": "2025-07-18T10:00:00Z", "equipment": "EQ-666", "quantity": "459 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (7, 1, 1, '{"step_id": "STP-0007", "actor": "user5", "timestamp": "2025-07-07T13:00:00Z", "equipment": "EQ-562", "quantity": "84 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (8, 1, 1, '{"step_id": "STP-0008", "actor": "user2", "timestamp": "2025-07-24T09:00:00Z", "equipment": "EQ-156", "quantity": "455 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (9, 1, 1, '{"step_id": "STP-0009", "actor": "user5", "timestamp": "2025-07-17T13:00:00Z", "equipment": "EQ-765", "quantity": "233 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (10, 1, 1, '{"step_id": "STP-0010", "actor": "user2", "timestamp": "2025-07-25T12:00:00Z", "equipment": "EQ-392", "quantity": "149 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (11, 1, 1, '{"step_id": "STP-0011", "actor": "user3", "timestamp": "2025-07-01T13:00:00Z", "equipment": "EQ-301", "quantity": "403 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (12, 1, 1, '{"step_id": "STP-0012", "actor": "user5", "timestamp": "2025-07-13T17:00:00Z", "equipment": "EQ-255", "quantity": "212 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (13, 1, 1, '{"step_id": "STP-0013", "actor": "user4", "timestamp": "2025-07-01T11:00:00Z", "equipment": "EQ-284", "quantity": "170 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (14, 1, 1, '{"step_id": "STP-0014", "actor": "user1", "timestamp": "2025-07-27T09:00:00Z", "equipment": "EQ-337", "quantity": "312 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (15, 1, 1, '{"step_id": "STP-0015", "actor": "user4", "timestamp": "2025-07-06T18:00:00Z", "equipment": "EQ-605", "quantity": "168 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (16, 1, 1, '{"step_id": "STP-0016", "actor": "user3", "timestamp": "2025-07-27T16:00:00Z", "equipment": "EQ-602", "quantity": "231 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (17, 1, 1, '{"step_id": "STP-0017", "actor": "user4", "timestamp": "2025-07-07T12:00:00Z", "equipment": "EQ-763", "quantity": "165 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (18, 1, 1, '{"step_id": "STP-0018", "actor": "user3", "timestamp": "2025-07-07T08:00:00Z", "equipment": "EQ-287", "quantity": "254 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (19, 1, 1, '{"step_id": "STP-0019", "actor": "user1", "timestamp": "2025-07-06T15:00:00Z", "equipment": "EQ-455", "quantity": "45 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (20, 1, 1, '{"step_id": "STP-0020", "actor": "user2", "timestamp": "2025-07-26T17:00:00Z", "equipment": "EQ-998", "quantity": "274 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (21, 1, 1, '{"step_id": "STP-0021", "actor": "user5", "timestamp": "2025-07-25T11:00:00Z", "equipment": "EQ-236", "quantity": "468 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (22, 1, 1, '{"step_id": "STP-0022", "actor": "user5", "timestamp": "2025-07-06T09:00:00Z", "equipment": "EQ-974", "quantity": "100 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (23, 1, 1, '{"step_id": "STP-0023", "actor": "user2", "timestamp": "2025-07-07T11:00:00Z", "equipment": "EQ-680", "quantity": "384 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (24, 1, 1, '{"step_id": "STP-0024", "actor": "user2", "timestamp": "2025-07-21T09:00:00Z", "equipment": "EQ-222", "quantity": "443 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (25, 1, 1, '{"step_id": "STP-0025", "actor": "user1", "timestamp": "2025-07-28T14:00:00Z", "equipment": "EQ-887", "quantity": "388 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (26, 1, 1, '{"step_id": "STP-0026", "actor": "user2", "timestamp": "2025-07-08T16:00:00Z", "equipment": "EQ-844", "quantity": "54 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (27, 1, 1, '{"step_id": "STP-0027", "actor": "user2", "timestamp": "2025-07-08T16:00:00Z", "equipment": "EQ-367", "quantity": "414 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (28, 1, 1, '{"step_id": "STP-0028", "actor": "user1", "timestamp": "2025-07-06T16:00:00Z", "equipment": "EQ-633", "quantity": "37 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (29, 1, 1, '{"step_id": "STP-0029", "actor": "user2", "timestamp": "2025-07-09T09:00:00Z", "equipment": "EQ-665", "quantity": "357 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (30, 1, 1, '{"step_id": "STP-0030", "actor": "user3", "timestamp": "2025-07-08T13:00:00Z", "equipment": "EQ-334", "quantity": "356 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (31, 1, 1, '{"step_id": "STP-0031", "actor": "user1", "timestamp": "2025-07-13T09:00:00Z", "equipment": "EQ-883", "quantity": "265 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (32, 1, 1, '{"step_id": "STP-0032", "actor": "user4", "timestamp": "2025-07-22T16:00:00Z", "equipment": "EQ-468", "quantity": "141 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (33, 1, 1, '{"step_id": "STP-0033", "actor": "user1", "timestamp": "2025-07-18T14:00:00Z", "equipment": "EQ-649", "quantity": "169 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (34, 1, 1, '{"step_id": "STP-0034", "actor": "user5", "timestamp": "2025-07-10T12:00:00Z", "equipment": "EQ-781", "quantity": "186 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (35, 1, 1, '{"step_id": "STP-0035", "actor": "user4", "timestamp": "2025-07-05T13:00:00Z", "equipment": "EQ-322", "quantity": "318 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (36, 1, 1, '{"step_id": "STP-0036", "actor": "user1", "timestamp": "2025-07-16T09:00:00Z", "equipment": "EQ-433", "quantity": "66 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (37, 1, 1, '{"step_id": "STP-0037", "actor": "user3", "timestamp": "2025-07-04T10:00:00Z", "equipment": "EQ-203", "quantity": "489 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (38, 1, 1, '{"step_id": "STP-0038", "actor": "user2", "timestamp": "2025-07-24T08:00:00Z", "equipment": "EQ-920", "quantity": "202 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (39, 1, 1, '{"step_id": "STP-0039", "actor": "user1", "timestamp": "2025-07-08T14:00:00Z", "equipment": "EQ-723", "quantity": "16 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (40, 1, 1, '{"step_id": "STP-0040", "actor": "user5", "timestamp": "2025-07-17T08:00:00Z", "equipment": "EQ-199", "quantity": "279 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (41, 1, 1, '{"step_id": "STP-0041", "actor": "user5", "timestamp": "2025-07-28T08:00:00Z", "equipment": "EQ-132", "quantity": "324 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (42, 1, 1, '{"step_id": "STP-0042", "actor": "user1", "timestamp": "2025-07-14T09:00:00Z", "equipment": "EQ-876", "quantity": "487 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (43, 1, 1, '{"step_id": "STP-0043", "actor": "user3", "timestamp": "2025-07-15T18:00:00Z", "equipment": "EQ-908", "quantity": "398 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (44, 1, 1, '{"step_id": "STP-0044", "actor": "user2", "timestamp": "2025-07-19T17:00:00Z", "equipment": "EQ-704", "quantity": "48 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (45, 1, 1, '{"step_id": "STP-0045", "actor": "user3", "timestamp": "2025-07-08T15:00:00Z", "equipment": "EQ-670", "quantity": "159 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (46, 1, 1, '{"step_id": "STP-0046", "actor": "user2", "timestamp": "2025-07-12T14:00:00Z", "equipment": "EQ-355", "quantity": "145 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (47, 1, 1, '{"step_id": "STP-0047", "actor": "user1", "timestamp": "2025-07-03T17:00:00Z", "equipment": "EQ-328", "quantity": "70 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (48, 1, 1, '{"step_id": "STP-0048", "actor": "user2", "timestamp": "2025-07-08T11:00:00Z", "equipment": "EQ-779", "quantity": "354 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (49, 1, 1, '{"step_id": "STP-0049", "actor": "user3", "timestamp": "2025-07-27T11:00:00Z", "equipment": "EQ-612", "quantity": "248 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (50, 1, 1, '{"step_id": "STP-0050", "actor": "user1", "timestamp": "2025-07-23T15:00:00Z", "equipment": "EQ-855", "quantity": "342 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (51, 1, 1, '{"step_id": "STP-0051", "actor": "user5", "timestamp": "2025-07-24T09:00:00Z", "equipment": "EQ-348", "quantity": "85 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (52, 1, 1, '{"step_id": "STP-0052", "actor": "user4", "timestamp": "2025-07-06T12:00:00Z", "equipment": "EQ-331", "quantity": "311 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (53, 1, 1, '{"step_id": "STP-0053", "actor": "user3", "timestamp": "2025-07-24T08:00:00Z", "equipment": "EQ-613", "quantity": "320 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (54, 1, 1, '{"step_id": "STP-0054", "actor": "user4", "timestamp": "2025-07-13T15:00:00Z", "equipment": "EQ-214", "quantity": "34 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (55, 1, 1, '{"step_id": "STP-0055", "actor": "user3", "timestamp": "2025-07-02T12:00:00Z", "equipment": "EQ-132", "quantity": "410 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (56, 1, 1, '{"step_id": "STP-0056", "actor": "user3", "timestamp": "2025-07-02T17:00:00Z", "equipment": "EQ-176", "quantity": "245 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (57, 1, 1, '{"step_id": "STP-0057", "actor": "user5", "timestamp": "2025-07-28T13:00:00Z", "equipment": "EQ-318", "quantity": "150 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (58, 1, 1, '{"step_id": "STP-0058", "actor": "user1", "timestamp": "2025-07-20T08:00:00Z", "equipment": "EQ-889", "quantity": "422 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (59, 1, 1, '{"step_id": "STP-0059", "actor": "user4", "timestamp": "2025-07-04T16:00:00Z", "equipment": "EQ-278", "quantity": "207 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (60, 1, 1, '{"step_id": "STP-0060", "actor": "user3", "timestamp": "2025-07-14T18:00:00Z", "equipment": "EQ-308", "quantity": "353 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (61, 1, 1, '{"step_id": "STP-0061", "actor": "user1", "timestamp": "2025-07-02T15:00:00Z", "equipment": "EQ-305", "quantity": "301 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (62, 1, 1, '{"step_id": "STP-0062", "actor": "user4", "timestamp": "2025-07-24T10:00:00Z", "equipment": "EQ-228", "quantity": "481 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (63, 1, 1, '{"step_id": "STP-0063", "actor": "user5", "timestamp": "2025-07-24T10:00:00Z", "equipment": "EQ-524", "quantity": "465 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (64, 1, 1, '{"step_id": "STP-0064", "actor": "user3", "timestamp": "2025-07-23T09:00:00Z", "equipment": "EQ-129", "quantity": "493 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (65, 1, 1, '{"step_id": "STP-0065", "actor": "user4", "timestamp": "2025-07-20T18:00:00Z", "equipment": "EQ-265", "quantity": "189 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (66, 1, 1, '{"step_id": "STP-0066", "actor": "user5", "timestamp": "2025-07-23T14:00:00Z", "equipment": "EQ-550", "quantity": "35 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (67, 1, 1, '{"step_id": "STP-0067", "actor": "user4", "timestamp": "2025-07-05T10:00:00Z", "equipment": "EQ-554", "quantity": "391 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (68, 1, 1, '{"step_id": "STP-0068", "actor": "user5", "timestamp": "2025-07-23T13:00:00Z", "equipment": "EQ-523", "quantity": "465 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (69, 1, 1, '{"step_id": "STP-0069", "actor": "user5", "timestamp": "2025-07-14T14:00:00Z", "equipment": "EQ-351", "quantity": "12 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (70, 1, 1, '{"step_id": "STP-0070", "actor": "user4", "timestamp": "2025-07-12T10:00:00Z", "equipment": "EQ-199", "quantity": "166 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (71, 1, 1, '{"step_id": "STP-0071", "actor": "user1", "timestamp": "2025-07-25T16:00:00Z", "equipment": "EQ-753", "quantity": "368 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (72, 1, 1, '{"step_id": "STP-0072", "actor": "user2", "timestamp": "2025-07-12T12:00:00Z", "equipment": "EQ-558", "quantity": "365 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (73, 1, 1, '{"step_id": "STP-0073", "actor": "user1", "timestamp": "2025-07-08T14:00:00Z", "equipment": "EQ-590", "quantity": "225 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (74, 1, 1, '{"step_id": "STP-0074", "actor": "user1", "timestamp": "2025-07-15T08:00:00Z", "equipment": "EQ-835", "quantity": "495 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (75, 1, 1, '{"step_id": "STP-0075", "actor": "user3", "timestamp": "2025-07-26T12:00:00Z", "equipment": "EQ-508", "quantity": "397 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (76, 1, 1, '{"step_id": "STP-0076", "actor": "user3", "timestamp": "2025-07-03T14:00:00Z", "equipment": "EQ-605", "quantity": "126 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (77, 1, 1, '{"step_id": "STP-0077", "actor": "user1", "timestamp": "2025-07-07T15:00:00Z", "equipment": "EQ-860", "quantity": "487 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (78, 1, 1, '{"step_id": "STP-0078", "actor": "user5", "timestamp": "2025-07-07T09:00:00Z", "equipment": "EQ-386", "quantity": "179 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (79, 1, 1, '{"step_id": "STP-0079", "actor": "user3", "timestamp": "2025-07-07T18:00:00Z", "equipment": "EQ-762", "quantity": "136 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (80, 1, 1, '{"step_id": "STP-0080", "actor": "user5", "timestamp": "2025-07-24T16:00:00Z", "equipment": "EQ-210", "quantity": "381 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (81, 1, 1, '{"step_id": "STP-0081", "actor": "user4", "timestamp": "2025-07-13T12:00:00Z", "equipment": "EQ-906", "quantity": "101 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (82, 1, 1, '{"step_id": "STP-0082", "actor": "user2", "timestamp": "2025-07-17T08:00:00Z", "equipment": "EQ-392", "quantity": "284 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (83, 1, 1, '{"step_id": "STP-0083", "actor": "user3", "timestamp": "2025-07-22T13:00:00Z", "equipment": "EQ-363", "quantity": "139 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (84, 1, 1, '{"step_id": "STP-0084", "actor": "user4", "timestamp": "2025-07-05T14:00:00Z", "equipment": "EQ-610", "quantity": "416 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (85, 1, 1, '{"step_id": "STP-0085", "actor": "user2", "timestamp": "2025-07-28T08:00:00Z", "equipment": "EQ-153", "quantity": "135 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (86, 1, 1, '{"step_id": "STP-0086", "actor": "user5", "timestamp": "2025-07-18T10:00:00Z", "equipment": "EQ-696", "quantity": "10 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (87, 1, 1, '{"step_id": "STP-0087", "actor": "user2", "timestamp": "2025-07-20T09:00:00Z", "equipment": "EQ-875", "quantity": "272 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (88, 1, 1, '{"step_id": "STP-0088", "actor": "user2", "timestamp": "2025-07-21T11:00:00Z", "equipment": "EQ-322", "quantity": "88 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (89, 1, 1, '{"step_id": "STP-0089", "actor": "user1", "timestamp": "2025-07-04T11:00:00Z", "equipment": "EQ-158", "quantity": "484 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (90, 1, 1, '{"step_id": "STP-0090", "actor": "user2", "timestamp": "2025-07-13T08:00:00Z", "equipment": "EQ-283", "quantity": "407 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (91, 1, 1, '{"step_id": "STP-0091", "actor": "user4", "timestamp": "2025-07-14T12:00:00Z", "equipment": "EQ-780", "quantity": "104 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (92, 1, 1, '{"step_id": "STP-0092", "actor": "user2", "timestamp": "2025-07-08T11:00:00Z", "equipment": "EQ-484", "quantity": "408 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (93, 1, 1, '{"step_id": "STP-0093", "actor": "user2", "timestamp": "2025-07-08T08:00:00Z", "equipment": "EQ-442", "quantity": "21 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (94, 1, 1, '{"step_id": "STP-0094", "actor": "user3", "timestamp": "2025-07-25T12:00:00Z", "equipment": "EQ-109", "quantity": "462 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (95, 1, 1, '{"step_id": "STP-0095", "actor": "user5", "timestamp": "2025-07-27T13:00:00Z", "equipment": "EQ-928", "quantity": "263 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (96, 1, 1, '{"step_id": "STP-0096", "actor": "user3", "timestamp": "2025-07-08T13:00:00Z", "equipment": "EQ-868", "quantity": "135 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (97, 1, 1, '{"step_id": "STP-0097", "actor": "user5", "timestamp": "2025-07-24T09:00:00Z", "equipment": "EQ-485", "quantity": "36 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (98, 1, 1, '{"step_id": "STP-0098", "actor": "user2", "timestamp": "2025-07-03T09:00:00Z", "equipment": "EQ-267", "quantity": "322 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (99, 1, 1, '{"step_id": "STP-0099", "actor": "user3", "timestamp": "2025-07-18T15:00:00Z", "equipment": "EQ-237", "quantity": "13 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (100, 1, 1, '{"step_id": "STP-0100", "actor": "user4", "timestamp": "2025-07-09T11:00:00Z", "equipment": "EQ-483", "quantity": "466 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (101, 1, 1, '{"step_id": "STP-0101", "actor": "user5", "timestamp": "2025-07-19T12:00:00Z", "equipment": "EQ-598", "quantity": "298 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (102, 1, 1, '{"step_id": "STP-0102", "actor": "user3", "timestamp": "2025-07-06T16:00:00Z", "equipment": "EQ-960", "quantity": "105 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (103, 1, 1, '{"step_id": "STP-0103", "actor": "user4", "timestamp": "2025-07-25T08:00:00Z", "equipment": "EQ-332", "quantity": "188 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (104, 1, 1, '{"step_id": "STP-0104", "actor": "user2", "timestamp": "2025-07-25T13:00:00Z", "equipment": "EQ-507", "quantity": "26 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (105, 1, 1, '{"step_id": "STP-0105", "actor": "user4", "timestamp": "2025-07-02T09:00:00Z", "equipment": "EQ-823", "quantity": "66 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (106, 1, 1, '{"step_id": "STP-0106", "actor": "user1", "timestamp": "2025-07-14T10:00:00Z", "equipment": "EQ-787", "quantity": "217 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (107, 1, 1, '{"step_id": "STP-0107", "actor": "user5", "timestamp": "2025-07-18T11:00:00Z", "equipment": "EQ-241", "quantity": "291 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (108, 1, 1, '{"step_id": "STP-0108", "actor": "user4", "timestamp": "2025-07-15T10:00:00Z", "equipment": "EQ-996", "quantity": "499 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (109, 1, 1, '{"step_id": "STP-0109", "actor": "user4", "timestamp": "2025-07-01T14:00:00Z", "equipment": "EQ-444", "quantity": "486 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (110, 1, 1, '{"step_id": "STP-0110", "actor": "user2", "timestamp": "2025-07-22T15:00:00Z", "equipment": "EQ-916", "quantity": "18 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (111, 1, 1, '{"step_id": "STP-0111", "actor": "user4", "timestamp": "2025-07-14T18:00:00Z", "equipment": "EQ-348", "quantity": "462 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (112, 1, 1, '{"step_id": "STP-0112", "actor": "user5", "timestamp": "2025-07-26T09:00:00Z", "equipment": "EQ-107", "quantity": "106 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (113, 1, 1, '{"step_id": "STP-0113", "actor": "user2", "timestamp": "2025-07-21T18:00:00Z", "equipment": "EQ-504", "quantity": "324 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (114, 1, 1, '{"step_id": "STP-0114", "actor": "user1", "timestamp": "2025-07-03T13:00:00Z", "equipment": "EQ-473", "quantity": "377 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (115, 1, 1, '{"step_id": "STP-0115", "actor": "user1", "timestamp": "2025-07-19T17:00:00Z", "equipment": "EQ-374", "quantity": "64 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (116, 1, 1, '{"step_id": "STP-0116", "actor": "user2", "timestamp": "2025-07-01T17:00:00Z", "equipment": "EQ-750", "quantity": "28 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (117, 1, 1, '{"step_id": "STP-0117", "actor": "user1", "timestamp": "2025-07-11T10:00:00Z", "equipment": "EQ-482", "quantity": "414 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (118, 1, 1, '{"step_id": "STP-0118", "actor": "user1", "timestamp": "2025-07-23T09:00:00Z", "equipment": "EQ-299", "quantity": "424 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (119, 1, 1, '{"step_id": "STP-0119", "actor": "user2", "timestamp": "2025-07-07T08:00:00Z", "equipment": "EQ-290", "quantity": "205 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (120, 1, 1, '{"step_id": "STP-0120", "actor": "user5", "timestamp": "2025-07-06T10:00:00Z", "equipment": "EQ-419", "quantity": "174 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (121, 1, 1, '{"step_id": "STP-0121", "actor": "user4", "timestamp": "2025-07-18T16:00:00Z", "equipment": "EQ-752", "quantity": "298 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (122, 1, 1, '{"step_id": "STP-0122", "actor": "user1", "timestamp": "2025-07-11T18:00:00Z", "equipment": "EQ-935", "quantity": "172 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (123, 1, 1, '{"step_id": "STP-0123", "actor": "user2", "timestamp": "2025-07-15T08:00:00Z", "equipment": "EQ-224", "quantity": "63 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (124, 1, 1, '{"step_id": "STP-0124", "actor": "user5", "timestamp": "2025-07-17T11:00:00Z", "equipment": "EQ-678", "quantity": "240 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (125, 1, 1, '{"step_id": "STP-0125", "actor": "user2", "timestamp": "2025-07-22T11:00:00Z", "equipment": "EQ-412", "quantity": "404 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (126, 1, 1, '{"step_id": "STP-0126", "actor": "user3", "timestamp": "2025-07-11T13:00:00Z", "equipment": "EQ-467", "quantity": "447 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (127, 1, 1, '{"step_id": "STP-0127", "actor": "user3", "timestamp": "2025-07-07T11:00:00Z", "equipment": "EQ-912", "quantity": "232 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (128, 1, 1, '{"step_id": "STP-0128", "actor": "user4", "timestamp": "2025-07-07T13:00:00Z", "equipment": "EQ-660", "quantity": "41 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (129, 1, 1, '{"step_id": "STP-0129", "actor": "user2", "timestamp": "2025-07-12T16:00:00Z", "equipment": "EQ-394", "quantity": "442 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (130, 1, 1, '{"step_id": "STP-0130", "actor": "user4", "timestamp": "2025-07-07T18:00:00Z", "equipment": "EQ-414", "quantity": "340 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (131, 1, 1, '{"step_id": "STP-0131", "actor": "user2", "timestamp": "2025-07-20T16:00:00Z", "equipment": "EQ-186", "quantity": "485 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (132, 1, 1, '{"step_id": "STP-0132", "actor": "user2", "timestamp": "2025-07-04T10:00:00Z", "equipment": "EQ-174", "quantity": "368 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (133, 1, 1, '{"step_id": "STP-0133", "actor": "user4", "timestamp": "2025-07-01T11:00:00Z", "equipment": "EQ-691", "quantity": "421 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (134, 1, 1, '{"step_id": "STP-0134", "actor": "user1", "timestamp": "2025-07-05T18:00:00Z", "equipment": "EQ-336", "quantity": "14 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (135, 1, 1, '{"step_id": "STP-0135", "actor": "user1", "timestamp": "2025-07-10T09:00:00Z", "equipment": "EQ-443", "quantity": "473 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (136, 1, 1, '{"step_id": "STP-0136", "actor": "user1", "timestamp": "2025-07-03T12:00:00Z", "equipment": "EQ-108", "quantity": "341 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (137, 1, 1, '{"step_id": "STP-0137", "actor": "user4", "timestamp": "2025-07-27T14:00:00Z", "equipment": "EQ-874", "quantity": "484 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (138, 1, 1, '{"step_id": "STP-0138", "actor": "user1", "timestamp": "2025-07-19T09:00:00Z", "equipment": "EQ-527", "quantity": "461 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (139, 1, 1, '{"step_id": "STP-0139", "actor": "user2", "timestamp": "2025-07-07T18:00:00Z", "equipment": "EQ-710", "quantity": "307 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (140, 1, 1, '{"step_id": "STP-0140", "actor": "user3", "timestamp": "2025-07-10T14:00:00Z", "equipment": "EQ-584", "quantity": "156 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (141, 1, 1, '{"step_id": "STP-0141", "actor": "user2", "timestamp": "2025-07-16T13:00:00Z", "equipment": "EQ-821", "quantity": "115 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (142, 1, 1, '{"step_id": "STP-0142", "actor": "user5", "timestamp": "2025-07-13T08:00:00Z", "equipment": "EQ-173", "quantity": "228 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (143, 1, 1, '{"step_id": "STP-0143", "actor": "user1", "timestamp": "2025-07-14T15:00:00Z", "equipment": "EQ-497", "quantity": "317 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (144, 1, 1, '{"step_id": "STP-0144", "actor": "user2", "timestamp": "2025-07-01T11:00:00Z", "equipment": "EQ-730", "quantity": "500 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (145, 1, 1, '{"step_id": "STP-0145", "actor": "user5", "timestamp": "2025-07-11T14:00:00Z", "equipment": "EQ-384", "quantity": "210 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (146, 1, 1, '{"step_id": "STP-0146", "actor": "user3", "timestamp": "2025-07-06T12:00:00Z", "equipment": "EQ-489", "quantity": "376 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (147, 1, 1, '{"step_id": "STP-0147", "actor": "user3", "timestamp": "2025-07-18T18:00:00Z", "equipment": "EQ-841", "quantity": "186 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (148, 1, 1, '{"step_id": "STP-0148", "actor": "user1", "timestamp": "2025-07-21T18:00:00Z", "equipment": "EQ-794", "quantity": "81 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (149, 1, 1, '{"step_id": "STP-0149", "actor": "user4", "timestamp": "2025-07-24T14:00:00Z", "equipment": "EQ-618", "quantity": "348 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (150, 1, 1, '{"step_id": "STP-0150", "actor": "user3", "timestamp": "2025-07-18T16:00:00Z", "equipment": "EQ-262", "quantity": "193 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (151, 1, 1, '{"step_id": "STP-0151", "actor": "user1", "timestamp": "2025-07-20T15:00:00Z", "equipment": "EQ-865", "quantity": "488 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (152, 1, 1, '{"step_id": "STP-0152", "actor": "user4", "timestamp": "2025-07-17T10:00:00Z", "equipment": "EQ-962", "quantity": "249 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (153, 1, 1, '{"step_id": "STP-0153", "actor": "user5", "timestamp": "2025-07-06T08:00:00Z", "equipment": "EQ-339", "quantity": "419 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (154, 1, 1, '{"step_id": "STP-0154", "actor": "user3", "timestamp": "2025-07-23T14:00:00Z", "equipment": "EQ-298", "quantity": "441 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (155, 1, 1, '{"step_id": "STP-0155", "actor": "user5", "timestamp": "2025-07-22T17:00:00Z", "equipment": "EQ-198", "quantity": "138 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (156, 1, 1, '{"step_id": "STP-0156", "actor": "user4", "timestamp": "2025-07-26T11:00:00Z", "equipment": "EQ-237", "quantity": "406 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (157, 1, 1, '{"step_id": "STP-0157", "actor": "user5", "timestamp": "2025-07-18T13:00:00Z", "equipment": "EQ-510", "quantity": "188 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (158, 1, 1, '{"step_id": "STP-0158", "actor": "user3", "timestamp": "2025-07-05T17:00:00Z", "equipment": "EQ-436", "quantity": "81 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (159, 1, 1, '{"step_id": "STP-0159", "actor": "user2", "timestamp": "2025-07-21T13:00:00Z", "equipment": "EQ-361", "quantity": "407 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (160, 1, 1, '{"step_id": "STP-0160", "actor": "user5", "timestamp": "2025-07-06T09:00:00Z", "equipment": "EQ-318", "quantity": "281 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (161, 1, 1, '{"step_id": "STP-0161", "actor": "user1", "timestamp": "2025-07-01T10:00:00Z", "equipment": "EQ-654", "quantity": "136 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (162, 1, 1, '{"step_id": "STP-0162", "actor": "user3", "timestamp": "2025-07-07T13:00:00Z", "equipment": "EQ-734", "quantity": "381 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (163, 1, 1, '{"step_id": "STP-0163", "actor": "user5", "timestamp": "2025-07-21T17:00:00Z", "equipment": "EQ-408", "quantity": "181 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (164, 1, 1, '{"step_id": "STP-0164", "actor": "user2", "timestamp": "2025-07-15T18:00:00Z", "equipment": "EQ-388", "quantity": "137 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (165, 1, 1, '{"step_id": "STP-0165", "actor": "user3", "timestamp": "2025-07-17T14:00:00Z", "equipment": "EQ-856", "quantity": "493 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (166, 1, 1, '{"step_id": "STP-0166", "actor": "user5", "timestamp": "2025-07-14T14:00:00Z", "equipment": "EQ-515", "quantity": "66 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (167, 1, 1, '{"step_id": "STP-0167", "actor": "user2", "timestamp": "2025-07-17T14:00:00Z", "equipment": "EQ-272", "quantity": "286 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (168, 1, 1, '{"step_id": "STP-0168", "actor": "user1", "timestamp": "2025-07-25T13:00:00Z", "equipment": "EQ-842", "quantity": "336 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (169, 1, 1, '{"step_id": "STP-0169", "actor": "user3", "timestamp": "2025-07-13T18:00:00Z", "equipment": "EQ-532", "quantity": "272 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (170, 1, 1, '{"step_id": "STP-0170", "actor": "user5", "timestamp": "2025-07-28T15:00:00Z", "equipment": "EQ-482", "quantity": "468 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (171, 1, 1, '{"step_id": "STP-0171", "actor": "user2", "timestamp": "2025-07-20T17:00:00Z", "equipment": "EQ-746", "quantity": "81 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (172, 1, 1, '{"step_id": "STP-0172", "actor": "user5", "timestamp": "2025-07-26T11:00:00Z", "equipment": "EQ-912", "quantity": "312 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (173, 1, 1, '{"step_id": "STP-0173", "actor": "user3", "timestamp": "2025-07-27T11:00:00Z", "equipment": "EQ-921", "quantity": "406 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (174, 1, 1, '{"step_id": "STP-0174", "actor": "user1", "timestamp": "2025-07-09T16:00:00Z", "equipment": "EQ-716", "quantity": "382 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (175, 1, 1, '{"step_id": "STP-0175", "actor": "user1", "timestamp": "2025-07-23T14:00:00Z", "equipment": "EQ-695", "quantity": "400 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (176, 1, 1, '{"step_id": "STP-0176", "actor": "user3", "timestamp": "2025-07-07T18:00:00Z", "equipment": "EQ-971", "quantity": "80 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (177, 1, 1, '{"step_id": "STP-0177", "actor": "user4", "timestamp": "2025-07-16T18:00:00Z", "equipment": "EQ-845", "quantity": "467 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (178, 1, 1, '{"step_id": "STP-0178", "actor": "user3", "timestamp": "2025-07-26T12:00:00Z", "equipment": "EQ-621", "quantity": "207 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (179, 1, 1, '{"step_id": "STP-0179", "actor": "user1", "timestamp": "2025-07-01T12:00:00Z", "equipment": "EQ-697", "quantity": "55 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (180, 1, 1, '{"step_id": "STP-0180", "actor": "user1", "timestamp": "2025-07-10T09:00:00Z", "equipment": "EQ-571", "quantity": "320 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (181, 1, 1, '{"step_id": "STP-0181", "actor": "user1", "timestamp": "2025-07-05T09:00:00Z", "equipment": "EQ-247", "quantity": "82 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (182, 1, 1, '{"step_id": "STP-0182", "actor": "user4", "timestamp": "2025-07-28T12:00:00Z", "equipment": "EQ-507", "quantity": "344 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (183, 1, 1, '{"step_id": "STP-0183", "actor": "user4", "timestamp": "2025-07-14T14:00:00Z", "equipment": "EQ-230", "quantity": "251 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (184, 1, 1, '{"step_id": "STP-0184", "actor": "user3", "timestamp": "2025-07-19T12:00:00Z", "equipment": "EQ-379", "quantity": "48 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (185, 1, 1, '{"step_id": "STP-0185", "actor": "user5", "timestamp": "2025-07-17T17:00:00Z", "equipment": "EQ-238", "quantity": "142 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (186, 1, 1, '{"step_id": "STP-0186", "actor": "user5", "timestamp": "2025-07-01T09:00:00Z", "equipment": "EQ-475", "quantity": "143 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (187, 1, 1, '{"step_id": "STP-0187", "actor": "user2", "timestamp": "2025-07-16T15:00:00Z", "equipment": "EQ-936", "quantity": "291 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (188, 1, 1, '{"step_id": "STP-0188", "actor": "user3", "timestamp": "2025-07-07T18:00:00Z", "equipment": "EQ-816", "quantity": "139 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (189, 1, 1, '{"step_id": "STP-0189", "actor": "user1", "timestamp": "2025-07-13T09:00:00Z", "equipment": "EQ-792", "quantity": "310 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (190, 1, 1, '{"step_id": "STP-0190", "actor": "user1", "timestamp": "2025-07-01T16:00:00Z", "equipment": "EQ-214", "quantity": "114 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (191, 1, 1, '{"step_id": "STP-0191", "actor": "user3", "timestamp": "2025-07-22T15:00:00Z", "equipment": "EQ-251", "quantity": "399 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (192, 1, 1, '{"step_id": "STP-0192", "actor": "user2", "timestamp": "2025-07-23T08:00:00Z", "equipment": "EQ-665", "quantity": "269 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (193, 1, 1, '{"step_id": "STP-0193", "actor": "user1", "timestamp": "2025-07-20T17:00:00Z", "equipment": "EQ-142", "quantity": "186 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (194, 1, 1, '{"step_id": "STP-0194", "actor": "user4", "timestamp": "2025-07-28T14:00:00Z", "equipment": "EQ-515", "quantity": "149 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (195, 1, 1, '{"step_id": "STP-0195", "actor": "user2", "timestamp": "2025-07-20T10:00:00Z", "equipment": "EQ-293", "quantity": "20 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (196, 1, 1, '{"step_id": "STP-0196", "actor": "user1", "timestamp": "2025-07-14T09:00:00Z", "equipment": "EQ-863", "quantity": "403 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (197, 1, 1, '{"step_id": "STP-0197", "actor": "user2", "timestamp": "2025-07-04T16:00:00Z", "equipment": "EQ-333", "quantity": "28 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (198, 1, 1, '{"step_id": "STP-0198", "actor": "user3", "timestamp": "2025-07-05T09:00:00Z", "equipment": "EQ-451", "quantity": "101 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (199, 1, 1, '{"step_id": "STP-0199", "actor": "user2", "timestamp": "2025-07-23T13:00:00Z", "equipment": "EQ-240", "quantity": "409 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (200, 1, 1, '{"step_id": "STP-0200", "actor": "user1", "timestamp": "2025-07-25T11:00:00Z", "equipment": "EQ-836", "quantity": "19 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (201, 1, 1, '{"step_id": "STP-0201", "actor": "user4", "timestamp": "2025-07-19T11:00:00Z", "equipment": "EQ-613", "quantity": "211 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (202, 1, 1, '{"step_id": "STP-0202", "actor": "user4", "timestamp": "2025-07-03T11:00:00Z", "equipment": "EQ-291", "quantity": "261 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (203, 1, 1, '{"step_id": "STP-0203", "actor": "user3", "timestamp": "2025-07-10T10:00:00Z", "equipment": "EQ-561", "quantity": "85 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (204, 1, 1, '{"step_id": "STP-0204", "actor": "user2", "timestamp": "2025-07-02T14:00:00Z", "equipment": "EQ-213", "quantity": "165 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (205, 1, 1, '{"step_id": "STP-0205", "actor": "user3", "timestamp": "2025-07-25T09:00:00Z", "equipment": "EQ-643", "quantity": "29 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (206, 1, 1, '{"step_id": "STP-0206", "actor": "user2", "timestamp": "2025-07-04T13:00:00Z", "equipment": "EQ-893", "quantity": "211 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (207, 1, 1, '{"step_id": "STP-0207", "actor": "user4", "timestamp": "2025-07-12T15:00:00Z", "equipment": "EQ-286", "quantity": "419 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (208, 1, 1, '{"step_id": "STP-0208", "actor": "user1", "timestamp": "2025-07-03T18:00:00Z", "equipment": "EQ-853", "quantity": "325 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (209, 1, 1, '{"step_id": "STP-0209", "actor": "user3", "timestamp": "2025-07-09T12:00:00Z", "equipment": "EQ-132", "quantity": "189 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (210, 1, 1, '{"step_id": "STP-0210", "actor": "user5", "timestamp": "2025-07-08T10:00:00Z", "equipment": "EQ-512", "quantity": "122 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (211, 1, 1, '{"step_id": "STP-0211", "actor": "user5", "timestamp": "2025-07-22T15:00:00Z", "equipment": "EQ-803", "quantity": "181 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (212, 1, 1, '{"step_id": "STP-0212", "actor": "user4", "timestamp": "2025-07-06T18:00:00Z", "equipment": "EQ-878", "quantity": "361 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (213, 1, 1, '{"step_id": "STP-0213", "actor": "user4", "timestamp": "2025-07-18T11:00:00Z", "equipment": "EQ-701", "quantity": "231 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (214, 1, 1, '{"step_id": "STP-0214", "actor": "user2", "timestamp": "2025-07-22T08:00:00Z", "equipment": "EQ-470", "quantity": "114 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (215, 1, 1, '{"step_id": "STP-0215", "actor": "user4", "timestamp": "2025-07-12T16:00:00Z", "equipment": "EQ-582", "quantity": "378 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (216, 1, 1, '{"step_id": "STP-0216", "actor": "user4", "timestamp": "2025-07-16T18:00:00Z", "equipment": "EQ-175", "quantity": "301 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (217, 1, 1, '{"step_id": "STP-0217", "actor": "user5", "timestamp": "2025-07-14T17:00:00Z", "equipment": "EQ-104", "quantity": "118 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (218, 1, 1, '{"step_id": "STP-0218", "actor": "user2", "timestamp": "2025-07-17T09:00:00Z", "equipment": "EQ-959", "quantity": "490 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (219, 1, 1, '{"step_id": "STP-0219", "actor": "user5", "timestamp": "2025-07-27T17:00:00Z", "equipment": "EQ-405", "quantity": "458 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (220, 1, 1, '{"step_id": "STP-0220", "actor": "user3", "timestamp": "2025-07-10T14:00:00Z", "equipment": "EQ-272", "quantity": "59 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (221, 1, 1, '{"step_id": "STP-0221", "actor": "user1", "timestamp": "2025-07-04T10:00:00Z", "equipment": "EQ-578", "quantity": "168 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (222, 1, 1, '{"step_id": "STP-0222", "actor": "user2", "timestamp": "2025-07-05T17:00:00Z", "equipment": "EQ-307", "quantity": "322 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (223, 1, 1, '{"step_id": "STP-0223", "actor": "user3", "timestamp": "2025-07-06T10:00:00Z", "equipment": "EQ-697", "quantity": "334 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (224, 1, 1, '{"step_id": "STP-0224", "actor": "user1", "timestamp": "2025-07-03T08:00:00Z", "equipment": "EQ-732", "quantity": "444 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (225, 1, 1, '{"step_id": "STP-0225", "actor": "user4", "timestamp": "2025-07-25T11:00:00Z", "equipment": "EQ-971", "quantity": "336 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (226, 1, 1, '{"step_id": "STP-0226", "actor": "user3", "timestamp": "2025-07-04T09:00:00Z", "equipment": "EQ-151", "quantity": "253 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (227, 1, 1, '{"step_id": "STP-0227", "actor": "user2", "timestamp": "2025-07-22T14:00:00Z", "equipment": "EQ-141", "quantity": "51 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (228, 1, 1, '{"step_id": "STP-0228", "actor": "user5", "timestamp": "2025-07-21T11:00:00Z", "equipment": "EQ-392", "quantity": "442 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (229, 1, 1, '{"step_id": "STP-0229", "actor": "user3", "timestamp": "2025-07-14T16:00:00Z", "equipment": "EQ-702", "quantity": "348 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (230, 1, 1, '{"step_id": "STP-0230", "actor": "user1", "timestamp": "2025-07-25T09:00:00Z", "equipment": "EQ-253", "quantity": "168 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (231, 1, 1, '{"step_id": "STP-0231", "actor": "user2", "timestamp": "2025-07-18T18:00:00Z", "equipment": "EQ-972", "quantity": "368 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (232, 1, 1, '{"step_id": "STP-0232", "actor": "user4", "timestamp": "2025-07-27T10:00:00Z", "equipment": "EQ-335", "quantity": "406 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (233, 1, 1, '{"step_id": "STP-0233", "actor": "user2", "timestamp": "2025-07-11T17:00:00Z", "equipment": "EQ-324", "quantity": "229 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (234, 1, 1, '{"step_id": "STP-0234", "actor": "user3", "timestamp": "2025-07-17T10:00:00Z", "equipment": "EQ-826", "quantity": "20 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (235, 1, 1, '{"step_id": "STP-0235", "actor": "user3", "timestamp": "2025-07-15T09:00:00Z", "equipment": "EQ-186", "quantity": "390 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (236, 1, 1, '{"step_id": "STP-0236", "actor": "user2", "timestamp": "2025-07-22T12:00:00Z", "equipment": "EQ-662", "quantity": "73 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (237, 1, 1, '{"step_id": "STP-0237", "actor": "user5", "timestamp": "2025-07-22T09:00:00Z", "equipment": "EQ-955", "quantity": "331 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (238, 1, 1, '{"step_id": "STP-0238", "actor": "user4", "timestamp": "2025-07-16T14:00:00Z", "equipment": "EQ-118", "quantity": "464 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (239, 1, 1, '{"step_id": "STP-0239", "actor": "user1", "timestamp": "2025-07-19T18:00:00Z", "equipment": "EQ-420", "quantity": "406 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (240, 1, 1, '{"step_id": "STP-0240", "actor": "user1", "timestamp": "2025-07-02T13:00:00Z", "equipment": "EQ-954", "quantity": "182 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (241, 1, 1, '{"step_id": "STP-0241", "actor": "user4", "timestamp": "2025-07-27T10:00:00Z", "equipment": "EQ-257", "quantity": "428 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (242, 1, 1, '{"step_id": "STP-0242", "actor": "user1", "timestamp": "2025-07-18T09:00:00Z", "equipment": "EQ-340", "quantity": "134 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (243, 1, 1, '{"step_id": "STP-0243", "actor": "user1", "timestamp": "2025-07-23T10:00:00Z", "equipment": "EQ-728", "quantity": "138 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (244, 1, 1, '{"step_id": "STP-0244", "actor": "user2", "timestamp": "2025-07-25T10:00:00Z", "equipment": "EQ-961", "quantity": "85 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (245, 1, 1, '{"step_id": "STP-0245", "actor": "user3", "timestamp": "2025-07-05T17:00:00Z", "equipment": "EQ-575", "quantity": "342 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (246, 1, 1, '{"step_id": "STP-0246", "actor": "user4", "timestamp": "2025-07-03T12:00:00Z", "equipment": "EQ-840", "quantity": "71 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (247, 1, 1, '{"step_id": "STP-0247", "actor": "user1", "timestamp": "2025-07-11T18:00:00Z", "equipment": "EQ-165", "quantity": "376 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (248, 1, 1, '{"step_id": "STP-0248", "actor": "user3", "timestamp": "2025-07-22T15:00:00Z", "equipment": "EQ-277", "quantity": "72 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (249, 1, 1, '{"step_id": "STP-0249", "actor": "user5", "timestamp": "2025-07-09T14:00:00Z", "equipment": "EQ-382", "quantity": "126 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (250, 1, 1, '{"step_id": "STP-0250", "actor": "user4", "timestamp": "2025-07-20T08:00:00Z", "equipment": "EQ-407", "quantity": "34 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (251, 1, 1, '{"step_id": "STP-0251", "actor": "user5", "timestamp": "2025-07-02T12:00:00Z", "equipment": "EQ-890", "quantity": "433 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (252, 1, 1, '{"step_id": "STP-0252", "actor": "user1", "timestamp": "2025-07-27T16:00:00Z", "equipment": "EQ-572", "quantity": "154 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (253, 1, 1, '{"step_id": "STP-0253", "actor": "user5", "timestamp": "2025-07-05T10:00:00Z", "equipment": "EQ-683", "quantity": "381 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (254, 1, 1, '{"step_id": "STP-0254", "actor": "user5", "timestamp": "2025-07-04T11:00:00Z", "equipment": "EQ-563", "quantity": "373 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (255, 1, 1, '{"step_id": "STP-0255", "actor": "user2", "timestamp": "2025-07-21T14:00:00Z", "equipment": "EQ-293", "quantity": "276 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (256, 1, 1, '{"step_id": "STP-0256", "actor": "user1", "timestamp": "2025-07-23T10:00:00Z", "equipment": "EQ-620", "quantity": "251 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (257, 1, 1, '{"step_id": "STP-0257", "actor": "user1", "timestamp": "2025-07-11T09:00:00Z", "equipment": "EQ-318", "quantity": "253 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (258, 1, 1, '{"step_id": "STP-0258", "actor": "user4", "timestamp": "2025-07-02T08:00:00Z", "equipment": "EQ-592", "quantity": "75 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (259, 1, 1, '{"step_id": "STP-0259", "actor": "user4", "timestamp": "2025-07-04T12:00:00Z", "equipment": "EQ-449", "quantity": "58 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (260, 1, 1, '{"step_id": "STP-0260", "actor": "user5", "timestamp": "2025-07-09T09:00:00Z", "equipment": "EQ-778", "quantity": "484 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (261, 1, 1, '{"step_id": "STP-0261", "actor": "user5", "timestamp": "2025-07-10T12:00:00Z", "equipment": "EQ-656", "quantity": "406 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (262, 1, 1, '{"step_id": "STP-0262", "actor": "user1", "timestamp": "2025-07-11T16:00:00Z", "equipment": "EQ-489", "quantity": "434 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (263, 1, 1, '{"step_id": "STP-0263", "actor": "user4", "timestamp": "2025-07-20T10:00:00Z", "equipment": "EQ-379", "quantity": "418 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (264, 1, 1, '{"step_id": "STP-0264", "actor": "user4", "timestamp": "2025-07-09T16:00:00Z", "equipment": "EQ-829", "quantity": "194 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (265, 1, 1, '{"step_id": "STP-0265", "actor": "user1", "timestamp": "2025-07-02T15:00:00Z", "equipment": "EQ-265", "quantity": "310 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (266, 1, 1, '{"step_id": "STP-0266", "actor": "user5", "timestamp": "2025-07-02T14:00:00Z", "equipment": "EQ-361", "quantity": "478 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (267, 1, 1, '{"step_id": "STP-0267", "actor": "user4", "timestamp": "2025-07-22T15:00:00Z", "equipment": "EQ-795", "quantity": "392 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (268, 1, 1, '{"step_id": "STP-0268", "actor": "user4", "timestamp": "2025-07-03T14:00:00Z", "equipment": "EQ-903", "quantity": "83 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (269, 1, 1, '{"step_id": "STP-0269", "actor": "user5", "timestamp": "2025-07-08T12:00:00Z", "equipment": "EQ-293", "quantity": "28 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (270, 1, 1, '{"step_id": "STP-0270", "actor": "user5", "timestamp": "2025-07-28T13:00:00Z", "equipment": "EQ-968", "quantity": "337 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (271, 1, 1, '{"step_id": "STP-0271", "actor": "user4", "timestamp": "2025-07-12T16:00:00Z", "equipment": "EQ-326", "quantity": "372 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (272, 1, 1, '{"step_id": "STP-0272", "actor": "user5", "timestamp": "2025-07-06T12:00:00Z", "equipment": "EQ-630", "quantity": "483 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (273, 1, 1, '{"step_id": "STP-0273", "actor": "user5", "timestamp": "2025-07-27T14:00:00Z", "equipment": "EQ-365", "quantity": "291 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (274, 1, 1, '{"step_id": "STP-0274", "actor": "user2", "timestamp": "2025-07-16T09:00:00Z", "equipment": "EQ-525", "quantity": "222 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (275, 1, 1, '{"step_id": "STP-0275", "actor": "user2", "timestamp": "2025-07-26T14:00:00Z", "equipment": "EQ-353", "quantity": "457 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (276, 1, 1, '{"step_id": "STP-0276", "actor": "user3", "timestamp": "2025-07-07T14:00:00Z", "equipment": "EQ-774", "quantity": "106 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (277, 1, 1, '{"step_id": "STP-0277", "actor": "user5", "timestamp": "2025-07-02T18:00:00Z", "equipment": "EQ-391", "quantity": "207 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (278, 1, 1, '{"step_id": "STP-0278", "actor": "user2", "timestamp": "2025-07-02T12:00:00Z", "equipment": "EQ-387", "quantity": "374 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (279, 1, 1, '{"step_id": "STP-0279", "actor": "user2", "timestamp": "2025-07-18T08:00:00Z", "equipment": "EQ-293", "quantity": "462 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (280, 1, 1, '{"step_id": "STP-0280", "actor": "user4", "timestamp": "2025-07-17T11:00:00Z", "equipment": "EQ-351", "quantity": "282 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (281, 1, 1, '{"step_id": "STP-0281", "actor": "user1", "timestamp": "2025-07-12T14:00:00Z", "equipment": "EQ-523", "quantity": "104 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (282, 1, 1, '{"step_id": "STP-0282", "actor": "user4", "timestamp": "2025-07-26T09:00:00Z", "equipment": "EQ-311", "quantity": "290 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (283, 1, 1, '{"step_id": "STP-0283", "actor": "user2", "timestamp": "2025-07-27T14:00:00Z", "equipment": "EQ-203", "quantity": "246 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (284, 1, 1, '{"step_id": "STP-0284", "actor": "user3", "timestamp": "2025-07-03T12:00:00Z", "equipment": "EQ-123", "quantity": "231 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (285, 1, 1, '{"step_id": "STP-0285", "actor": "user5", "timestamp": "2025-07-15T09:00:00Z", "equipment": "EQ-927", "quantity": "187 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (286, 1, 1, '{"step_id": "STP-0286", "actor": "user2", "timestamp": "2025-07-18T08:00:00Z", "equipment": "EQ-789", "quantity": "56 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (287, 1, 1, '{"step_id": "STP-0287", "actor": "user2", "timestamp": "2025-07-08T17:00:00Z", "equipment": "EQ-881", "quantity": "36 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (288, 1, 1, '{"step_id": "STP-0288", "actor": "user3", "timestamp": "2025-07-27T16:00:00Z", "equipment": "EQ-204", "quantity": "407 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (289, 1, 1, '{"step_id": "STP-0289", "actor": "user5", "timestamp": "2025-07-21T12:00:00Z", "equipment": "EQ-396", "quantity": "318 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (290, 1, 1, '{"step_id": "STP-0290", "actor": "user3", "timestamp": "2025-07-11T09:00:00Z", "equipment": "EQ-719", "quantity": "386 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (291, 1, 1, '{"step_id": "STP-0291", "actor": "user3", "timestamp": "2025-07-11T09:00:00Z", "equipment": "EQ-285", "quantity": "240 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (292, 1, 1, '{"step_id": "STP-0292", "actor": "user1", "timestamp": "2025-07-06T17:00:00Z", "equipment": "EQ-120", "quantity": "162 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (293, 1, 1, '{"step_id": "STP-0293", "actor": "user5", "timestamp": "2025-07-09T12:00:00Z", "equipment": "EQ-445", "quantity": "173 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (294, 1, 1, '{"step_id": "STP-0294", "actor": "user5", "timestamp": "2025-07-04T09:00:00Z", "equipment": "EQ-818", "quantity": "369 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (295, 1, 1, '{"step_id": "STP-0295", "actor": "user5", "timestamp": "2025-07-28T18:00:00Z", "equipment": "EQ-846", "quantity": "179 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (296, 1, 1, '{"step_id": "STP-0296", "actor": "user5", "timestamp": "2025-07-17T12:00:00Z", "equipment": "EQ-145", "quantity": "470 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (297, 1, 1, '{"step_id": "STP-0297", "actor": "user4", "timestamp": "2025-07-17T11:00:00Z", "equipment": "EQ-293", "quantity": "238 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (298, 1, 1, '{"step_id": "STP-0298", "actor": "user3", "timestamp": "2025-07-24T17:00:00Z", "equipment": "EQ-889", "quantity": "356 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (299, 1, 1, '{"step_id": "STP-0299", "actor": "user4", "timestamp": "2025-07-02T16:00:00Z", "equipment": "EQ-837", "quantity": "65 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');
INSERT INTO sample_records (id, run_id, llm_id, content, generation_prompt)
VALUES (300, 1, 1, '{"step_id": "STP-0300", "actor": "user5", "timestamp": "2025-07-08T15:00:00Z", "equipment": "EQ-186", "quantity": "50 mg", "notes": "Step completed successfully."}'::jsonb, 'Generate a valid manufacturing record.');

-- Insert injected deviations
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (1, 69, 'D001');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (2, 176, 'D001');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (3, 249, 'D002');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (4, 168, 'D002');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (5, 247, 'D003');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (6, 22, 'D003');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (7, 240, 'D004');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (8, 223, 'D004');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (9, 7, 'D005');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (10, 186, 'D005');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (11, 73, 'D006');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (12, 156, 'D006');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (13, 177, 'D007');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (14, 254, 'D007');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (15, 191, 'D008');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (16, 161, 'D008');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (17, 106, 'D009');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (18, 153, 'D009');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (19, 103, 'D010');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (20, 96, 'D010');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (21, 67, 'D011');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (22, 259, 'D011');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (23, 299, 'D012');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (24, 28, 'D012');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (25, 183, 'D013');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (26, 175, 'D013');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (27, 182, 'D014');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (28, 132, 'D014');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (29, 227, 'D015');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (30, 297, 'D015');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (31, 202, 'D016');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (32, 178, 'D016');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (33, 238, 'D017');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (34, 298, 'D017');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (35, 262, 'D018');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (36, 245, 'D018');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (37, 70, 'D019');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (38, 14, 'D019');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (39, 133, 'D020');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (40, 252, 'D020');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (41, 65, 'D021');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (42, 242, 'D021');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (43, 72, 'D022');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (44, 52, 'D022');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (45, 229, 'D023');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (46, 300, 'D023');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (47, 192, 'D024');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (48, 126, 'D024');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (49, 41, 'D025');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (50, 264, 'D025');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (51, 85, 'D026');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (52, 29, 'D026');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (53, 266, 'D027');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (54, 114, 'D027');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (55, 100, 'D028');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (56, 50, 'D028');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (57, 80, 'D029');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (58, 149, 'D029');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (59, 84, 'D030');
INSERT INTO injected_deviations (id, sample_record_id, deviation_type_id)
VALUES (60, 188, 'D030');