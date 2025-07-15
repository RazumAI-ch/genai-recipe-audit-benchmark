--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.training_examples DROP CONSTRAINT training_examples_source_sample_id_fkey;
ALTER TABLE ONLY public.training_example_deviations DROP CONSTRAINT training_example_deviations_training_example_id_fkey;
ALTER TABLE ONLY public.training_example_deviations DROP CONSTRAINT training_example_deviations_deviation_type_id_fkey;
ALTER TABLE ONLY public.sample_records DROP CONSTRAINT sample_records_run_id_fkey;
ALTER TABLE ONLY public.sample_records DROP CONSTRAINT sample_records_llm_id_fkey;
ALTER TABLE ONLY public.run_llm_results DROP CONSTRAINT run_llm_results_run_id_fkey;
ALTER TABLE ONLY public.run_llm_results DROP CONSTRAINT run_llm_results_llm_id_fkey;
ALTER TABLE ONLY public.record_eval_results DROP CONSTRAINT record_eval_results_sample_record_id_fkey;
ALTER TABLE ONLY public.record_eval_results DROP CONSTRAINT record_eval_results_run_id_fkey;
ALTER TABLE ONLY public.record_eval_results DROP CONSTRAINT record_eval_results_llm_id_fkey;
ALTER TABLE ONLY public.injected_deviations DROP CONSTRAINT injected_deviations_sample_record_id_fkey;
ALTER TABLE ONLY public.injected_deviations DROP CONSTRAINT injected_deviations_deviation_type_id_fkey;
ALTER TABLE ONLY public.training_runs DROP CONSTRAINT training_runs_pkey;
ALTER TABLE ONLY public.training_examples DROP CONSTRAINT training_examples_pkey;
ALTER TABLE ONLY public.training_example_deviations DROP CONSTRAINT training_example_deviations_pkey;
ALTER TABLE ONLY public.schema_docs DROP CONSTRAINT schema_docs_pkey;
ALTER TABLE ONLY public.sample_records DROP CONSTRAINT sample_records_pkey;
ALTER TABLE ONLY public.run_llm_results DROP CONSTRAINT run_llm_results_pkey;
ALTER TABLE ONLY public.record_eval_results DROP CONSTRAINT record_eval_results_run_id_llm_id_sample_record_id_key;
ALTER TABLE ONLY public.record_eval_results DROP CONSTRAINT record_eval_results_pkey;
ALTER TABLE ONLY public.llms DROP CONSTRAINT llms_pkey;
ALTER TABLE ONLY public.injected_deviations DROP CONSTRAINT injected_deviations_pkey;
ALTER TABLE ONLY public.deviation_types DROP CONSTRAINT deviation_types_pkey;
ALTER TABLE ONLY public.benchmark_runs DROP CONSTRAINT benchmark_runs_pkey;
ALTER TABLE public.training_examples ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.sample_records ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.run_llm_results ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.record_eval_results ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.llms ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.injected_deviations ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.benchmark_runs ALTER COLUMN id DROP DEFAULT;
DROP TABLE public.training_runs;
DROP SEQUENCE public.training_examples_id_seq;
DROP TABLE public.training_examples;
DROP TABLE public.training_example_deviations;
DROP TABLE public.schema_docs;
DROP SEQUENCE public.sample_records_id_seq;
DROP TABLE public.sample_records;
DROP SEQUENCE public.run_llm_results_id_seq;
DROP TABLE public.run_llm_results;
DROP SEQUENCE public.record_eval_results_id_seq;
DROP TABLE public.record_eval_results;
DROP SEQUENCE public.llms_id_seq;
DROP TABLE public.llms;
DROP SEQUENCE public.injected_deviations_id_seq;
DROP TABLE public.injected_deviations;
DROP TABLE public.deviation_types;
DROP SEQUENCE public.benchmark_runs_id_seq;
DROP TABLE public.benchmark_runs;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: benchmark_runs; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.benchmark_runs (
    id integer NOT NULL,
    run_name text,
    sample_size integer,
    run_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.benchmark_runs OWNER TO benchmark;

--
-- Name: benchmark_runs_id_seq; Type: SEQUENCE; Schema: public; Owner: benchmark
--

CREATE SEQUENCE public.benchmark_runs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.benchmark_runs_id_seq OWNER TO benchmark;

--
-- Name: benchmark_runs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benchmark
--

ALTER SEQUENCE public.benchmark_runs_id_seq OWNED BY public.benchmark_runs.id;


--
-- Name: deviation_types; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.deviation_types (
    id text NOT NULL,
    type text NOT NULL,
    alcoa_principle text NOT NULL,
    description text NOT NULL,
    severity text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.deviation_types OWNER TO benchmark;

--
-- Name: injected_deviations; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.injected_deviations (
    id integer NOT NULL,
    sample_record_id integer,
    deviation_type_id text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.injected_deviations OWNER TO benchmark;

--
-- Name: injected_deviations_id_seq; Type: SEQUENCE; Schema: public; Owner: benchmark
--

CREATE SEQUENCE public.injected_deviations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.injected_deviations_id_seq OWNER TO benchmark;

--
-- Name: injected_deviations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benchmark
--

ALTER SEQUENCE public.injected_deviations_id_seq OWNED BY public.injected_deviations.id;


--
-- Name: llms; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.llms (
    id integer NOT NULL,
    name text NOT NULL,
    provider text NOT NULL,
    model text NOT NULL,
    config_name text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    training_method text,
    model_path text,
    source_training_run uuid,
    logical_name text,
    updated_at timestamp without time zone DEFAULT now(),
    model_type text,
    is_active boolean DEFAULT true,
    notes text
);


ALTER TABLE public.llms OWNER TO benchmark;

--
-- Name: llms_id_seq; Type: SEQUENCE; Schema: public; Owner: benchmark
--

CREATE SEQUENCE public.llms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.llms_id_seq OWNER TO benchmark;

--
-- Name: llms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benchmark
--

ALTER SEQUENCE public.llms_id_seq OWNED BY public.llms.id;


--
-- Name: record_eval_results; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.record_eval_results (
    id integer NOT NULL,
    run_id integer,
    llm_id integer,
    sample_record_id integer,
    detected_deviation_ids text[] NOT NULL,
    deviation_explanations jsonb,
    evaluation_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.record_eval_results OWNER TO benchmark;

--
-- Name: record_eval_results_id_seq; Type: SEQUENCE; Schema: public; Owner: benchmark
--

CREATE SEQUENCE public.record_eval_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.record_eval_results_id_seq OWNER TO benchmark;

--
-- Name: record_eval_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benchmark
--

ALTER SEQUENCE public.record_eval_results_id_seq OWNED BY public.record_eval_results.id;


--
-- Name: run_llm_results; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.run_llm_results (
    id integer NOT NULL,
    run_id integer,
    llm_id integer,
    eval_duration_seconds real,
    token_input integer,
    token_output integer,
    prompt_price_per_1k numeric(10,6),
    completion_price_per_1k numeric(10,6),
    infra_price_per_hour numeric(10,4),
    cost_source text,
    estimated_cost_usd numeric(10,4),
    gxp1_score real,
    gxp2_score real,
    gxp3_score real,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.run_llm_results OWNER TO benchmark;

--
-- Name: run_llm_results_id_seq; Type: SEQUENCE; Schema: public; Owner: benchmark
--

CREATE SEQUENCE public.run_llm_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.run_llm_results_id_seq OWNER TO benchmark;

--
-- Name: run_llm_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benchmark
--

ALTER SEQUENCE public.run_llm_results_id_seq OWNED BY public.run_llm_results.id;


--
-- Name: sample_records; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.sample_records (
    id integer NOT NULL,
    run_id integer,
    llm_id integer,
    content jsonb NOT NULL,
    generation_prompt text,
    injected_deviation_ids text[],
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.sample_records OWNER TO benchmark;

--
-- Name: sample_records_id_seq; Type: SEQUENCE; Schema: public; Owner: benchmark
--

CREATE SEQUENCE public.sample_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sample_records_id_seq OWNER TO benchmark;

--
-- Name: sample_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benchmark
--

ALTER SEQUENCE public.sample_records_id_seq OWNED BY public.sample_records.id;


--
-- Name: schema_docs; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.schema_docs (
    table_name text NOT NULL,
    column_name text NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.schema_docs OWNER TO benchmark;

--
-- Name: training_example_deviations; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.training_example_deviations (
    training_example_id integer NOT NULL,
    deviation_type_id text NOT NULL,
    explanation text,
    source_field text NOT NULL
);


ALTER TABLE public.training_example_deviations OWNER TO benchmark;

--
-- Name: training_examples; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.training_examples (
    id integer NOT NULL,
    input_format text NOT NULL,
    input_content text NOT NULL,
    source_sample_id integer,
    source_llm text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT training_examples_input_format_check CHECK ((input_format = ANY (ARRAY['json'::text, 'csv'::text])))
);


ALTER TABLE public.training_examples OWNER TO benchmark;

--
-- Name: training_examples_id_seq; Type: SEQUENCE; Schema: public; Owner: benchmark
--

CREATE SEQUENCE public.training_examples_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.training_examples_id_seq OWNER TO benchmark;

--
-- Name: training_examples_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: benchmark
--

ALTER SEQUENCE public.training_examples_id_seq OWNED BY public.training_examples.id;


--
-- Name: training_runs; Type: TABLE; Schema: public; Owner: benchmark
--

CREATE TABLE public.training_runs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    model_name text NOT NULL,
    method text NOT NULL,
    dataset_description text,
    total_samples integer,
    total_tokens integer,
    epochs integer,
    hardware text,
    start_time timestamp without time zone,
    duration_seconds integer,
    final_loss double precision,
    final_accuracy double precision,
    log_path text,
    model_output_path text,
    notes text,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.training_runs OWNER TO benchmark;

--
-- Name: benchmark_runs id; Type: DEFAULT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.benchmark_runs ALTER COLUMN id SET DEFAULT nextval('public.benchmark_runs_id_seq'::regclass);


--
-- Name: injected_deviations id; Type: DEFAULT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.injected_deviations ALTER COLUMN id SET DEFAULT nextval('public.injected_deviations_id_seq'::regclass);


--
-- Name: llms id; Type: DEFAULT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.llms ALTER COLUMN id SET DEFAULT nextval('public.llms_id_seq'::regclass);


--
-- Name: record_eval_results id; Type: DEFAULT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.record_eval_results ALTER COLUMN id SET DEFAULT nextval('public.record_eval_results_id_seq'::regclass);


--
-- Name: run_llm_results id; Type: DEFAULT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.run_llm_results ALTER COLUMN id SET DEFAULT nextval('public.run_llm_results_id_seq'::regclass);


--
-- Name: sample_records id; Type: DEFAULT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.sample_records ALTER COLUMN id SET DEFAULT nextval('public.sample_records_id_seq'::regclass);


--
-- Name: training_examples id; Type: DEFAULT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.training_examples ALTER COLUMN id SET DEFAULT nextval('public.training_examples_id_seq'::regclass);


--
-- Name: benchmark_runs benchmark_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.benchmark_runs
    ADD CONSTRAINT benchmark_runs_pkey PRIMARY KEY (id);


--
-- Name: deviation_types deviation_types_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.deviation_types
    ADD CONSTRAINT deviation_types_pkey PRIMARY KEY (id);


--
-- Name: injected_deviations injected_deviations_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.injected_deviations
    ADD CONSTRAINT injected_deviations_pkey PRIMARY KEY (id);


--
-- Name: llms llms_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.llms
    ADD CONSTRAINT llms_pkey PRIMARY KEY (id);


--
-- Name: record_eval_results record_eval_results_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.record_eval_results
    ADD CONSTRAINT record_eval_results_pkey PRIMARY KEY (id);


--
-- Name: record_eval_results record_eval_results_run_id_llm_id_sample_record_id_key; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.record_eval_results
    ADD CONSTRAINT record_eval_results_run_id_llm_id_sample_record_id_key UNIQUE (run_id, llm_id, sample_record_id);


--
-- Name: run_llm_results run_llm_results_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.run_llm_results
    ADD CONSTRAINT run_llm_results_pkey PRIMARY KEY (id);


--
-- Name: sample_records sample_records_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.sample_records
    ADD CONSTRAINT sample_records_pkey PRIMARY KEY (id);


--
-- Name: schema_docs schema_docs_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.schema_docs
    ADD CONSTRAINT schema_docs_pkey PRIMARY KEY (table_name, column_name);


--
-- Name: training_example_deviations training_example_deviations_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.training_example_deviations
    ADD CONSTRAINT training_example_deviations_pkey PRIMARY KEY (training_example_id, deviation_type_id);


--
-- Name: training_examples training_examples_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.training_examples
    ADD CONSTRAINT training_examples_pkey PRIMARY KEY (id);


--
-- Name: training_runs training_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.training_runs
    ADD CONSTRAINT training_runs_pkey PRIMARY KEY (id);


--
-- Name: injected_deviations injected_deviations_deviation_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.injected_deviations
    ADD CONSTRAINT injected_deviations_deviation_type_id_fkey FOREIGN KEY (deviation_type_id) REFERENCES public.deviation_types(id);


--
-- Name: injected_deviations injected_deviations_sample_record_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.injected_deviations
    ADD CONSTRAINT injected_deviations_sample_record_id_fkey FOREIGN KEY (sample_record_id) REFERENCES public.sample_records(id) ON DELETE CASCADE;


--
-- Name: record_eval_results record_eval_results_llm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.record_eval_results
    ADD CONSTRAINT record_eval_results_llm_id_fkey FOREIGN KEY (llm_id) REFERENCES public.llms(id) ON DELETE CASCADE;


--
-- Name: record_eval_results record_eval_results_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.record_eval_results
    ADD CONSTRAINT record_eval_results_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.benchmark_runs(id) ON DELETE CASCADE;


--
-- Name: record_eval_results record_eval_results_sample_record_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.record_eval_results
    ADD CONSTRAINT record_eval_results_sample_record_id_fkey FOREIGN KEY (sample_record_id) REFERENCES public.sample_records(id) ON DELETE CASCADE;


--
-- Name: run_llm_results run_llm_results_llm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.run_llm_results
    ADD CONSTRAINT run_llm_results_llm_id_fkey FOREIGN KEY (llm_id) REFERENCES public.llms(id) ON DELETE CASCADE;


--
-- Name: run_llm_results run_llm_results_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.run_llm_results
    ADD CONSTRAINT run_llm_results_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.benchmark_runs(id) ON DELETE CASCADE;


--
-- Name: sample_records sample_records_llm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.sample_records
    ADD CONSTRAINT sample_records_llm_id_fkey FOREIGN KEY (llm_id) REFERENCES public.llms(id) ON DELETE CASCADE;


--
-- Name: sample_records sample_records_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.sample_records
    ADD CONSTRAINT sample_records_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.benchmark_runs(id) ON DELETE CASCADE;


--
-- Name: training_example_deviations training_example_deviations_deviation_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.training_example_deviations
    ADD CONSTRAINT training_example_deviations_deviation_type_id_fkey FOREIGN KEY (deviation_type_id) REFERENCES public.deviation_types(id);


--
-- Name: training_example_deviations training_example_deviations_training_example_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.training_example_deviations
    ADD CONSTRAINT training_example_deviations_training_example_id_fkey FOREIGN KEY (training_example_id) REFERENCES public.training_examples(id) ON DELETE CASCADE;


--
-- Name: training_examples training_examples_source_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: benchmark
--

ALTER TABLE ONLY public.training_examples
    ADD CONSTRAINT training_examples_source_sample_id_fkey FOREIGN KEY (source_sample_id) REFERENCES public.sample_records(id);


--
-- PostgreSQL database dump complete
--

