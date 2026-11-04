-- Grounding store for the taxonomy discovery pipeline (US 311617 / grounding trial).
-- PostgreSQL 14+ with the pgvector extension. {DIM} is replaced with the embedding size at load time.
CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS grounding_link, grounding_result, candidate, report_sentence, report, industry_definition, icao_category CASCADE;

-- Level 1 parents: the closed list the pipeline may ground to (CICTT, US 311617 IN-2)
CREATE TABLE icao_category (
  code          text PRIMARY KEY,
  name          text NOT NULL,
  definition    text NOT NULL,
  in_scope      boolean NOT NULL,
  co_code_only  boolean NOT NULL DEFAULT false,
  version       text NOT NULL,
  embedding     vector({DIM}) NOT NULL
);

-- Industry definitions with their SME-approved crosswalk to CICTT parents (I-8)
CREATE TABLE industry_definition (
  def_id     text PRIMARY KEY,
  source     text NOT NULL,
  term       text NOT NULL,
  body       text NOT NULL,
  parents    text[] NOT NULL,
  version    text NOT NULL,
  embedding  vector({DIM}) NOT NULL,
  tsv        tsvector GENERATED ALWAYS AS (to_tsvector('english', term || ' ' || body)) STORED
);

-- Reports (D1b) with their stage-2 multi-label Level 1 codes
CREATE TABLE report (
  report_key    text PRIMARY KEY,
  source_id     text NOT NULL,
  phase         text,
  l1_codes      text[] NOT NULL,
  source_codes  text,
  narrative     text NOT NULL,
  embedding     vector({DIM}) NOT NULL,
  tsv           tsvector GENERATED ALWAYS AS (to_tsvector('english', narrative || ' ' || coalesce(source_codes, ''))) STORED
);

-- Sentence-level vectors so evidence can be quoted exactly
CREATE TABLE report_sentence (
  report_key  text REFERENCES report(report_key),
  seq         int,
  sentence    text NOT NULL,
  embedding   vector({DIM}) NOT NULL,
  PRIMARY KEY (report_key, seq)
);

-- Candidate sub-categories from discovery (stage 3)
CREATE TABLE candidate (
  candidate_id     text PRIMARY KEY,
  name             text NOT NULL,
  definition       text NOT NULL,
  proposed_parent  text,
  embedding        vector({DIM}) NOT NULL
);

-- Results: one row per candidate per run, plus one row per link in the chain
CREATE TABLE grounding_result (
  run_id          text,
  candidate_id    text REFERENCES candidate(candidate_id),
  parent_code     text REFERENCES icao_category(code),
  parent_changed  boolean,
  status          text,           -- grounded | needs_review | not_grounded
  checks          jsonb,
  PRIMARY KEY (run_id, candidate_id)
);
CREATE TABLE grounding_link (
  run_id        text,
  candidate_id  text,
  link_type     text,             -- parent | definition | report
  target_id     text,
  score         real,
  evidence      text              -- exact quote for report links
);

CREATE INDEX ON report USING gin (tsv);
CREATE INDEX ON report USING gin (l1_codes);
CREATE INDEX ON industry_definition USING gin (parents);
-- For large corpora add approximate indexes, e.g.:
-- CREATE INDEX ON report USING hnsw (embedding vector_cosine_ops);
-- CREATE INDEX ON report_sentence USING hnsw (embedding vector_cosine_ops);
