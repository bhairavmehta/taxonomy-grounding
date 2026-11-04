# Grounding trial – taxonomy categories → ICAO parent → industry definitions → reports

This folder runs the grounding approach described in *Taxonomy Grounding Approach* (Word document). For each candidate category from discovery, it finds and checks three links:

1. **ICAO parent**: one CICTT Level 1 category, chosen only from the in-scope list.
2. **Industry definitions**: the definitions the category draws on, chosen only from those crosswalked to that parent.
3. **Supporting reports**: reports already coded to that parent, each with an evidence sentence quoted word for word.

It works in three steps:
- **Retrieve:** hybrid search in PostgreSQL with pgvector, combining vector similarity and full-text keywords.
- **Constrain:** choose only from closed sets.
- **Verify:** eight deterministic checks, G1 to G8.

Every candidate ends as *grounded*, *needs review* or *not grounded*.

> The sample reports in `data/sample_reports.json` are **synthetic**, written for the trial. The definitions are short paraphrases. Run the trial again on real extracts and official definition text in the approved environment.

## Files

| File | What it is |
|---|---|
| `run_trial.py` | Runs the trial and writes all outputs |
| `grounding.py` | Embedders, PostgreSQL/pgvector store, retrieval, constrained selection, sibling rule, verifier, prompt builder |
| `db/schema.sql` | Tables: icao_category, industry_definition, report, report_sentence, candidate, grounding_result, grounding_link |
| `prompts/constrained_grounding.md` | The constrained prompt for an LLM (filled per candidate with the retrieved context) |
| `prompts/grounding_output.schema.json` | The JSON the LLM must return |
| `interactive.py` | Interactive mode: type a candidate and watch it go through the five steps (exact pipeline) |
| `tools/combine_datasets.py` | Merges data folders (for example `data` + `data_sample_b` → `data_combined`) and records overlapping candidates |
| `tools/generate_sample_b.py` | Generates a larger synthetic sample (Sample B) with planted hard cases |
| `make_figures.py` | Approach figure, grounding chain for one candidate, results matrix |
| `data/` | Parents (CICTT), industry definitions with crosswalk, sample reports, candidates with the answer key |
| `out/` | Results of the last run (see below) |
| `viewer/grounding_viewer.html` | Interactive viewer: open in a browser, then use Load results to render your own out/ and data/ files |
| `start_local_db.sh` | Starts a throw-away local PostgreSQL with pgvector (Linux/macOS) |

## Run it

1. Install the packages: `pip install -r requirements.txt`.
2. Get a database. Either:
   - use a PostgreSQL 14+ database with the `vector` extension (ask the platform team), or
   - run `./start_local_db.sh`, which needs PostgreSQL and pgvector installed locally.
3. Run the trial:
   ```
   python run_trial.py --db postgresql://USER:PASSWORD@HOST:5432/DBNAME
   python make_figures.py                   # figures into out/
   python make_figures.py --candidate C5    # chain figure for another candidate
   ```

### Interactive mode – type your own candidate

```
python interactive.py --db postgresql://USER:PASSWORD@HOST:5432/DBNAME              # uses data/
python interactive.py --db ... --data data_sample_b --out out_sample_b --step       # pause after each step
python interactive.py --db ... --name "Fuel truck on the runway" --definition "A vehicle entered an active runway without clearance." --proposed RI
```

You are asked for a name, a definition and, optionally, the parent proposed by discovery. The candidate then goes through the same five steps as the trial, and each step is printed:
1. **Retrieve:** the closest reports.
2. **Parent:** the score for each parent.
3. **Definitions:** the crosswalked definitions.
4. **Support:** the supporting reports, each with its exact evidence sentence.
5. **Verify:** checks G1–G8, then the status.

Leave the name blank to quit. Every candidate is saved to `<out>/interactive/manual_results.json`, which the viewer opens with Load results (as the *Typed* view). The sibling rule needs the whole candidate set, so it is not applied to typed candidates.

The viewer also has a **Try a candidate** tab that runs the same steps in the browser on whatever data is loaded. It has a step-through mode and sliders for the main settings. Its vectors are word-based rather than pgvector embeddings, so the scores differ slightly: on the two samples it picks the same parent as the pipeline for 36 of 37 candidates, and the same status for 32 of 37. It reads the settings stored in the loaded results.

### Options

| Option | What it does |
|---|---|
| `--data FOLDER`, `--out FOLDER` | Use another dataset and output folder (for example `data_sample_b`, `out_sample_b`) |
| `--max-reports N`, `--min-support N` | Change the cap on supporting reports and the G5 floor for this run |
| `--model NAME_OR_PATH` | Use a sentence-transformers model (for example a local copy of SafeAeroBERT) instead of the built-in stand-in |
| `--prompts-only` | Fill the constrained prompt for every candidate into `out/prompts/` and stop |
| `--llm codex` | Send each prompt to Codex (`codex exec`, read-only) and verify its JSON answers |
| `--llm-outputs FOLDER` | Verify and score JSON answers from any LLM (one `C1.json` … per candidate; candidates without a file are left out) |

The default embedder is a local stand-in (TF-IDF reduced to 64 dimensions with SVD), used because no model could be downloaded in the build environment. Use a proper embedding model for real runs.

## Outputs (`out/`)

| File | Contents |
|---|---|
| `grounding_results.json` | Everything: links, diagnostics, checks, metrics, settings |
| `grounding_table.csv` | One row per candidate: parent, definitions, reports, status, failed checks |
| `grounding_cards.md` | A readable card per candidate with the full chain and quotes |
| `parent_selection.csv` | Parent choice by definitions only, report vote only, and hybrid |
| `guardrail_tests.csv` | Six bad answers an unconstrained LLM might give, and how the verifier treats them |
| `*_llm.*` | The same files for LLM answers (`--llm` or `--llm-outputs`) |
| `prompts/`, `llm_answers/` | Filled prompts, and the constrained-prompt answers used in the trial |
| `fig1_approach.png`, `fig2_chain_C1.png`, `fig3_results.png` | Figures |

The database also keeps `grounding_result` (one row per candidate) and `grounding_link` (one row per link) for each run.

## Checks

| ID | Check | If it fails |
|---|---|---|
| G1 | Parent is an allowed, in-scope CICTT category | Not grounded |
| G2 | Definitions exist and are crosswalked to the parent | Not grounded |
| G3 | Every report exists and is coded to the parent | Not grounded |
| G4 | Every evidence quote appears word for word in its report | Not grounded |
| G5 | At least `min_support` valid reports (3 in the trial; 10 in production) | Not grounded |
| G6 | At least 60% of the closest reports sit under the parent | Needs review |
| G7 | The chosen parent beats the runner-up by at least 0.10 | Needs review |
| G8 | The parent matches the one proposed by discovery | Needs review |

The settings are in `SETTINGS` at the top of `grounding.py`. They were tuned once on the synthetic sample; set them again on SME-labelled test sets (I-10).
