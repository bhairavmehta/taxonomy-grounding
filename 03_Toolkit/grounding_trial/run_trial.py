"""
run_trial.py – grounding trial: tie each candidate category to its ICAO parent, industry definitions and supporting reports.

Usage
  python run_trial.py                                   # local Postgres at postgresql://grounding@localhost:5433/grounding
  python run_trial.py --db postgresql://user:pw@host:5432/db
  python run_trial.py --model <sentence-transformers model>   # e.g. a local copy of SafeAeroBERT, if available
  python run_trial.py --prompts-only                    # write the filled LLM prompts to out/prompts/ and stop
  python run_trial.py --llm codex                       # ask Codex to ground each candidate (constrained prompt), then verify

Inputs  data/icao_categories.json, data/industry_definitions.json, data/sample_reports.json, data/candidates.json
Outputs out/grounding_results.json, out/grounding_table.csv, out/grounding_cards.md, out/parent_selection.csv,
        out/guardrail_tests.csv, and the grounding_result / grounding_link tables in the database.
"""
import argparse
import csv
import datetime as dt
import json
import os
import subprocess
import tempfile
from pathlib import Path

import grounding as G

ROOT = Path(__file__).parent
DATA, OUT = ROOT / "data", ROOT / "out"


def load_json(name, key):
    return json.loads((DATA / name).read_text(encoding="utf-8"))[key]


def call_codex(prompt):
    with tempfile.TemporaryDirectory() as tmp:
        last = Path(tmp) / "last.txt"
        cmd = [os.environ.get("CODEX_BIN", "codex"), "exec", "--sandbox", "read-only", "--skip-git-repo-check",
               "--output-last-message", str(last), "-"]
        subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=900, check=True)
        txt = last.read_text(encoding="utf-8")
    start, end = txt.find("{"), txt.rfind("}")
    return json.loads(txt[start:end + 1])


def main():
    global DATA, OUT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.environ.get("GROUNDING_DB", "postgresql://grounding@localhost:5433/grounding"))
    ap.add_argument("--max-reports", type=int, help=f"most supporting reports per candidate (default {G.SETTINGS['max_reports']})")
    ap.add_argument("--min-support", type=int, help=f"G5 floor (default {G.SETTINGS['min_support']})")
    ap.add_argument("--model", help="sentence-transformers model name or local path (default: local LSA stand-in)")
    ap.add_argument("--llm", choices=["codex"], help="use an LLM with the constrained prompt instead of the deterministic selector")
    ap.add_argument("--data", default=str(ROOT / "data"), help="folder with icao_categories.json, industry_definitions.json, sample_reports.json, candidates.json")
    ap.add_argument("--out", default=str(ROOT / "out"), help="folder for outputs")
    ap.add_argument("--prompts-only", action="store_true")
    ap.add_argument("--llm-outputs", help="folder of JSON answers (one <candidate_id>.json per candidate) from any LLM, to verify and score")
    args = ap.parse_args()
    if args.max_reports: G.SETTINGS["max_reports"] = args.max_reports
    if args.min_support: G.SETTINGS["min_support"] = args.min_support
    DATA, OUT = Path(args.data), Path(args.out)
    OUT.mkdir(parents=True, exist_ok=True)

    parents = load_json("icao_categories.json", "categories")
    defs = load_json("industry_definitions.json", "definitions")
    reports = load_json("sample_reports.json", "reports")
    cands = load_json("candidates.json", "candidates")

    corpus = ([f"{p['name']}. {p['definition']}" for p in parents] + [f"{d['term']}. {d['text']}" for d in defs]
              + [r["narrative"] for r in reports] + [f"{c['name']}. {c['definition']}" for c in cands])
    emb = G.SentenceTransformerEmbedder(args.model) if args.model else G.LocalEmbedder(corpus)
    store = G.Store(args.db)
    store.load((ROOT / "db" / "schema.sql").read_text(), emb, parents, defs, reports, cands)
    lookup = store.lookup()
    run_id = dt.datetime.now().strftime("run-%Y%m%d-%H%M%S")
    print(f"Loaded {len(parents)} parents, {len(defs)} definitions, {len(reports)} reports, {len(cands)} candidates "
          f"into pgvector (embedder {emb.name}, {emb.dim} dims). Run {run_id}")

    if args.prompts_only or args.llm or args.llm_outputs:
        tpl = (ROOT / "prompts" / "constrained_grounding.md").read_text(encoding="utf-8")
        (OUT / "prompts").mkdir(exist_ok=True)
        for c in cands:
            (OUT / "prompts" / f"{c['candidate_id']}.md").write_text(G.build_prompt(tpl, store, c["candidate_id"]), encoding="utf-8")
        print(f"Wrote {len(cands)} prompts to out/prompts/")
        if args.prompts_only:
            return

    results = []
    grounded = [G.ground_candidate(store, c["candidate_id"]) for c in cands]
    mode = "llm-codex" if args.llm else ("llm-file" if args.llm_outputs else "deterministic")
    if mode == "deterministic":
        G.resolve_siblings(grounded)
    for c, (out, diag) in zip(cands, grounded):
        cid = c["candidate_id"]
        if args.llm:
            out = call_codex((OUT / "prompts" / f"{cid}.md").read_text(encoding="utf-8"))
        elif args.llm_outputs:
            f = Path(args.llm_outputs) / f"{cid}.json"
            if not f.exists():          # no LLM answer for this candidate: leave it out of the LLM run
                continue
            out = json.loads(f.read_text(encoding="utf-8"))
        status, checks = G.verify(out, lookup, c["proposed_parent"], diag)
        results.append(dict(candidate=c, output=out, diag=diag, status=status, checks=[ch.__dict__ for ch in checks]))
        store.q("INSERT INTO grounding_result VALUES (%s,%s,%s,%s,%s,%s)",
                (run_id, cid, out["parent_code"], out["parent_code"] != c["proposed_parent"], status,
                 json.dumps([ch.__dict__ for ch in checks])))
        store.q("INSERT INTO grounding_link VALUES (%s,%s,'parent',%s,%s,NULL)", (run_id, cid, out["parent_code"], diag["parent_scores"].get(out["parent_code"])))
        for d in out["definition_ids"]:
            store.q("INSERT INTO grounding_link VALUES (%s,%s,'definition',%s,NULL,NULL)", (run_id, cid, d))
        for s in out["supporting_reports"]:
            store.q("INSERT INTO grounding_link VALUES (%s,%s,'report',%s,%s,%s)", (run_id, cid, s["report_key"], None, s["evidence"]))
        mark = {"grounded": "GROUNDED", "needs_review": "REVIEW", "not_grounded": "NOT GROUNDED"}[status]
        print(f"  {cid} {c['name'][:52]:<52} -> {out['parent_code']:<6} defs {len(out['definition_ids'])}  reports {len(out['supporting_reports'])}  {mark}")

    # score against the hand-labelled answer key
    tp = fp = fn = 0
    for r in results:
        got = {s["report_key"] for s in r["output"]["supporting_reports"]}
        exp = set(r["candidate"].get("expected_reports", []))
        r["metrics"] = dict(tp=len(got & exp), fp=sorted(got - exp), fn=sorted(exp - got),
                            parent_correct=r["output"]["parent_code"] == r["candidate"]["expected_parent"])
        tp, fp, fn = tp + len(got & exp), fp + len(got - exp), fn + len(exp - got)
    # second score: a report linked to an overlapping candidate (same events, other batch) is not an error
    exp_of = {r["candidate"]["candidate_id"]: set(r["candidate"].get("expected_reports", [])) for r in results}
    got_of = {r["candidate"]["candidate_id"]: {s["report_key"] for s in r["output"]["supporting_reports"]} for r in results}
    gtp = gfp = gfn = 0
    for r in results:
        cid = r["candidate"]["candidate_id"]; grp = [cid] + r["candidate"].get("overlaps", [])
        exp_g = set().union(*(exp_of.get(x, set()) for x in grp)); got_g = set().union(*(got_of.get(x, set()) for x in grp))
        got, exp = got_of[cid], exp_of[cid]
        gtp += len(got & exp_g); gfp += len(got - exp_g); gfn += len(exp - got_g)
    has_overlaps = any(r["candidate"].get("overlaps") for r in results)
    summary = dict(mode=mode, candidates=len(results),
                   status={s: sum(r["status"] == s for r in results) for s in ("grounded", "needs_review", "not_grounded")},
                   parent_correct=sum(r["metrics"]["parent_correct"] for r in results),
                   report_precision=round(tp / (tp + fp), 3) if tp + fp else None,
                   report_recall=round(tp / (tp + fn), 3) if tp + fn else None, tp=tp, fp=fp, fn=fn)
    if has_overlaps:
        summary.update(overlap_precision=round(gtp / (gtp + gfp), 3) if gtp + gfp else None,
                       overlap_recall=round(gtp / (gtp + gfn), 3) if gtp + gfn else None)
    print(f"  {mode}: parents correct {summary['parent_correct']}/{len(results)}; report links precision "
          f"{summary['report_precision']:.0%}, recall {summary['report_recall']:.0%} (tp {tp}, fp {fp}, fn {fn}); status {summary['status']}")
    if has_overlaps:
        print(f"  counting overlapping candidates: precision {summary['overlap_precision']:.0%}, recall {summary['overlap_recall']:.0%}")
    sfx = "" if mode == "deterministic" else "_llm"
    json.dump(dict(run_id=run_id, mode=mode, embedder=emb.name, dims=emb.dim, settings=G.SETTINGS, summary=summary, results=results),
              open(OUT / f"grounding_results{sfx}.json", "w"), indent=1, default=str)

    # table
    with open(OUT / f"grounding_table{sfx}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["candidate_id", "candidate", "proposed_parent", "grounded_parent", "expected_parent", "definitions", "supporting_reports", "status", "failed_checks"])
        for r in results:
            c, o = r["candidate"], r["output"]
            w.writerow([c["candidate_id"], c["name"], c["proposed_parent"], o["parent_code"], c["expected_parent"],
                        " ".join(o["definition_ids"]), " ".join(s["report_key"] for s in o["supporting_reports"]), r["status"],
                        " ".join(ch["id"] for ch in r["checks"] if not ch["passed"])])

    # cards
    dmap = {d["id"]: d for d in defs}
    pmap = {p["code"]: p for p in parents}
    rmap = {r["report_key"]: r for r in reports}
    L = [f"# Grounding cards – {run_id}", "", f"Embedder: {emb.name} ({emb.dim} dims). Sample reports are synthetic.", ""]
    for r in results:
        c, o, d = r["candidate"], r["output"], r["diag"]
        L += [f"## {c['candidate_id']} {c['name']}  –  {r['status'].replace('_', ' ').upper()}", "",
              f"*Candidate definition:* {c['definition']}", "",
              f"**ICAO parent:** {o['parent_code']} – {pmap.get(o['parent_code'], {}).get('name', 'NOT ALLOWED')} (proposed by discovery: {c['proposed_parent']}; "
              f"parent scores {d['parent_scores']}; agreement {d['parent_agreement']:.0%}"
              + (f"; suggested co-codes {', '.join(d['co_codes'])}" if d['co_codes'] else "") + ")", ""]
        if d.get("moved_to_sibling"):
            L += ["*Reports given to a better-matching sibling:* " + ", ".join(f"{k} → {o}" for k, o in d["moved_to_sibling"]), ""]
        L += ["**Industry definitions:**"] + [f"- {i} – {dmap[i]['term']} ({dmap[i]['source']})" if i in dmap else f"- {i} – NOT FOUND" for i in o["definition_ids"]] + [""]
        L += ["**Supporting reports:**"] + [f"- {s['report_key']} [{', '.join(rmap[s['report_key']]['l1_codes']) if s['report_key'] in rmap else 'NOT FOUND'}]: \"{s['evidence']}\"" for s in o["supporting_reports"]] + [""]
        if o.get("concerns"):
            L += [f"*Concerns:* {o['concerns']}", ""]
        L += ["**Checks:** " + " · ".join(f"{ch['id']} {'pass' if ch['passed'] else 'FAIL'}" for ch in r["checks"]), ""]
    (OUT / f"grounding_cards{sfx}.md").write_text("\n".join(L), encoding="utf-8")

    if mode != "deterministic":
        print(f"Outputs in {OUT}/ (suffix _llm)")
        return
    # parent selection: definitions only vs report vote only vs hybrid
    rows = []
    for mode in ("definition_only", "vote_only", "hybrid"):
        ok = 0
        for c in cands:
            o, _ = G.ground_candidate(store, c["candidate_id"], mode=mode)
            ok += o["parent_code"] == c["expected_parent"]
            rows.append([mode, c["candidate_id"], o["parent_code"], c["expected_parent"], o["parent_code"] == c["expected_parent"]])
        print(f"  parent selection, {mode:<16}: {ok}/{len(cands)} correct")
    with open(OUT / "parent_selection.csv", "w", newline="") as f:
        csv.writer(f).writerows([["mode", "candidate_id", "chosen", "expected", "correct"]] + rows)

    # guardrail tests: outputs an unconstrained LLM might give, checked by the same verifier
    first = next((r for r in results if r["status"] == "grounded"), results[0])
    base = first["output"]
    par = base["parent_code"]
    other_def = next(d["id"] for d in defs if par not in d["parents"])
    other_rep = next(x for x in reports if par not in x["l1_codes"])
    tests = [
        ("Parent not in the allowed list", dict(base, parent_code="RUNWAY-SAFETY")),
        ("Invented definition id", dict(base, definition_ids=base["definition_ids"] + ["IND-99"])),
        ("Definition from another parent", dict(base, definition_ids=[other_def])),
        ("Paraphrased evidence", dict(base, supporting_reports=[dict(base["supporting_reports"][0], evidence="The crew landed on a taxiway at night.")] + base["supporting_reports"][1:])),
        ("Report from another parent", dict(base, supporting_reports=base["supporting_reports"] + [dict(report_key=other_rep["report_key"], evidence=G.sentences(other_rep["narrative"])[0])])),
        ("Invented report key", dict(base, supporting_reports=base["supporting_reports"] + [dict(report_key="UNKNOWN-999", evidence="Invented evidence sentence.")])),
    ]
    with open(OUT / "guardrail_tests.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["test", "status", "failed_checks", "base_candidate"])
        for name, o in tests:
            st, ch = G.verify(o, lookup)
            w.writerow([name, st, " ".join(x.id for x in ch if not x.passed), first["candidate"]["candidate_id"]])
            print(f"  guardrail: {name:<34} -> {st} ({' '.join(x.id for x in ch if not x.passed)})")
    print(f"Outputs in {OUT}/")


if __name__ == "__main__":
    main()
