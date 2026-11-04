# Taxonomy Grounding – full package

**User story:** Investigate how to ground the taxonomy against ICAO categories and industry definitions
**Parent:** #311596 – Taxonomy discovery pipeline · **Author:** Bhairav Mehta (US) · **Date:** November 3, 2026

This package holds everything for the story:
- the documented grounding approach;
- the trial that links each candidate category → ICAO parent → industry definitions → supporting reports;
- the toolkit that runs it;
- an interactive viewer for reviewers.

> All reports in this package are **synthetic**: written by hand or generated from templates for the trial. They are not real events. Industry definitions are short paraphrases of the named sources. Rerun on real extracts and official definition text in the approved environment.

## Contents

| Folder | What it holds | Start with |
|---|---|---|
| `01_Document/` | *Taxonomy Grounding Approach* (Word and Markdown, 13 pages) and its figures | `Taxonomy_Grounding_Approach.docx` |
| `02_Viewer/` | Grounding Trial Viewer: one HTML file that works offline, with all 37 candidates built in | Open `grounding_viewer.html` in Chrome or Edge |
| `03_Toolkit/grounding_trial/` | Code, database schema, prompts, all three datasets and their results | `README.md` in that folder |
| `04_Load_Packs/` | Ready-made result sets for the viewer's **Load results** button | `README.md` in that folder |

## Evidence the story asked for

| Evidence | Where |
|---|---|
| Grounding approach selected and documented | Document §3 Options, §4 Selected approach, §11 Decisions (DG-1 to DG-4) |
| Retrieval over definitions and reports in pgvector | Document §4.1, §5 Data model · `grounding.py`, `db/schema.sql` |
| Constrained prompting | Document §4.2, Appendix B · `prompts/constrained_grounding.md`, `prompts/grounding_output.schema.json` |
| Agent workflows | Document §3, §4.4 (escalation only) |
| Trial: category → ICAO parent → industry definitions → supporting reports | Document §6, Figures 2–3, Appendix A · `out/`, `out_sample_b/`, `out_combined/` · Viewer |
| Each candidate ties back to its parent, definitions and supporting reports | Viewer → Candidates (the grounding chain for every candidate) · `grounding_cards.md` in each output folder |
| Bad links are caught | Document §6.4 · Viewer → Guardrail tests · `guardrail_tests.csv` |

## Results at a glance

| Run | Candidates | Reports | Parents correct | Precision | Recall | Grounded / review / not grounded |
|---|---|---|---|---|---|---|
| Trial | 9 | 36 | 8 | 97% | 97% | 6 / 2 / 1 |
| Sample B | 28 | 273 | 27 | 93% | 90% | 20 / 6 / 2 |
| Combined (viewer default) | 37 | 309 | 35 | 83% (89%*) | 79% (84%*) | 23 / 9 / 5 |

\* Counting overlaps: a report given to an overlapping candidate from the other batch is not counted as an error. In every run, all six guardrail tests (invented or misplaced links, paraphrased quotes) were blocked.

## Quick start

**Just look:** open `02_Viewer/grounding_viewer.html`. Its tabs:
- **Candidates:** the full chain for each candidate;
- **Check matrix:** every candidate against checks G1–G8;
- **Rules vs prompt:** the rules selector against the constrained-prompt answers;
- **Guardrail tests** and **Parent selection;**
- **Data:** every report, definition and parent;
- **Try a candidate:** type your own candidate and step through the process.

**Run it** (Python 3.10+, PostgreSQL 14+ with pgvector):

```bash
cd 03_Toolkit/grounding_trial
pip install -r requirements.txt
./start_local_db.sh                                   # or use your own pgvector database

# the trial (9 candidates)
python run_trial.py --db postgresql://grounding@localhost:5433/grounding

# the combined set (37 candidates): constrained-prompt answers first, then the rules run
createdb -h localhost -p 5433 -U grounding combined
python run_trial.py --db postgresql://grounding@localhost:5433/combined --data data_combined --out out_combined --max-reports 12 --llm-outputs out/llm_answers
python run_trial.py --db postgresql://grounding@localhost:5433/combined --data data_combined --out out_combined --max-reports 12

# type a candidate and follow it step by step
python interactive.py --db postgresql://grounding@localhost:5433/combined --data data_combined --out out_combined --max-reports 12 --step
```

Then load the files from `out_combined/` and `data_combined/` into the viewer with **Load results**.

**Make more synthetic data:**

```bash
python tools/generate_sample_b.py --seed 11 --scale 2 --background 100 --out data_sample_c
python tools/combine_datasets.py --inputs data data_sample_b data_sample_c --out data_all
```

## Key findings for review

1. **Approach:** retrieve (pgvector, hybrid vector and keyword search) → constrain (closed sets only) → verify (eight deterministic checks). Agents are used for escalation only.
2. **The reports' own codes matter most for choosing the parent.** Definition fit alone gets 26 of 37 parents right; adding the vote of the closest reports gets 35.
3. **Weak cases go to SMEs instead of being published:** wrong proposed parents, thin categories, ties between parents and low agreement.
4. **Merge duplicate candidates before grounding.** Candidates from different batches that describe the same events compete for the same reports.
5. **Limits:** synthetic data, a stand-in embedding model, and settings tuned on the sample. The next step is a real, SME-labelled sample of about 500 reports (Document §10).
