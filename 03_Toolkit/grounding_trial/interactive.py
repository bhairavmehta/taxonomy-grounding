"""
interactive.py – type a candidate category and watch it go through the grounding process step by step.

Usage
  python interactive.py                                  # prompts for name, definition and proposed parent
  python interactive.py --data data_sample_b             # use another dataset
  python interactive.py --name "Bird strike on climb-out" --definition "Bird or wildlife strike ..." --proposed BIRD
  python interactive.py --model <sentence-transformers model>

Each candidate you enter is grounded with exactly the same code as run_trial.py:
  Step 1 RETRIEVE  closest reports (hybrid vector + keyword search, no parent filter) -> parent vote
  Step 2 PARENT    0.3 x definition fit + 0.7 x report vote; margin over the runner-up
  Step 3 DEFINE    industry definitions crosswalked to that parent
  Step 4 SUPPORT   reports already coded to that parent, each with an exact evidence sentence
  Step 5 VERIFY    checks G1-G8 -> grounded / needs review / not grounded

Results are saved to <out>/interactive/manual_results.json, which the viewer can open with Load results.
Note: the sibling rule (a report supports only one candidate under the same parent) needs the whole
candidate set, so it is not applied to a single typed candidate.
"""
import argparse
import datetime as dt
import json
import os
import sys
import textwrap
from pathlib import Path

import grounding as G

ROOT = Path(__file__).parent
USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def c(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def bold(t): return c(t, "1")
def dim(t): return c(t, "2")
def green(t): return c(t, "32")
def amber(t): return c(t, "33")
def red(t): return c(t, "31")


def wrap(text, indent=6, width=100):
    return textwrap.fill(text, width=width, initial_indent=" " * indent, subsequent_indent=" " * indent)


def pause(args):
    if args.step and sys.stdin.isatty():
        input(dim("      press Enter for the next step…"))


def ask(prompt, default=None):
    try:
        v = input(prompt).strip()
    except EOFError:
        return default
    return v or default


def ground_typed(store, emb, lookup, pmap, dmap, rmap, name, definition, proposed, cid, args):
    vec = emb.encode([f"{name}. {definition}"])[0]
    store.q("DELETE FROM candidate WHERE candidate_id = %s", (cid,))
    store.q("INSERT INTO candidate VALUES (%s,%s,%s,%s,%s)", (cid, name, definition, proposed, vec))
    out, diag = G.ground_candidate(store, cid)
    S = G.SETTINGS
    p = out["parent_code"]

    print()
    print(bold(f"━━ {cid}  {name}"))
    print(wrap(definition))
    print(dim(f"      proposed parent: {proposed or '(none)'}"))

    # Step 1 – retrieve
    print(); print(bold("Step 1  RETRIEVE – closest reports, no parent filter (they vote on the parent)"))
    print(dim(f"      hybrid score = {S['vector_weight']} × vector cosine + {1 - S['vector_weight']:.1f} × keyword rank; "
              f"kept if ≥ {S['relative_cutoff']} × top score and ≥ {S['min_score']}"))
    for r in diag["pool"]:
        print(f"      {r['report_key']:<11} {r['score']:.2f}  coded {', '.join(r['l1'])}")
    if not diag["pool"]:
        print(red("      no report passed the cut-off"))
    pause(args)

    # Step 2 – parent
    print(); print(bold("Step 2  PARENT – pick one in-scope CICTT category"))
    print(dim(f"      parent score = {S['parent_def_weight']} × definition fit + {1 - S['parent_def_weight']:.1f} × report vote"))
    for k, v in diag["parent_scores"].items():
        tag = green("  ← chosen") if k == p else ""
        print(f"      {k:<7} {v:.3f}  {pmap.get(k, {}).get('name', '')}{tag}")
    print(f"      agreement {diag['parent_agreement']:.0%} of the pool is coded {p};  margin {diag['margin']:.2f} over {diag['runner_up']}")
    if diag["co_codes"]:
        print(f"      suggested co-codes: {', '.join(diag['co_codes'])}")
    pause(args)

    # Step 3 – definitions
    print(); print(bold(f"Step 3  DEFINE – industry definitions crosswalked to {p}"))
    for d in diag["definitions"]:
        print(f"      {d['def_id']:<7} {d['score']:.2f}  {d['term']} ({d['source']})")
    if not diag["definitions"]:
        print(red(f"      no definition crosswalked to {p} passed the cut-off"))
    pause(args)

    # Step 4 – support
    print(); print(bold(f"Step 4  SUPPORT – reports already coded to {p}, with an exact evidence sentence"))
    for s in diag["support"]:
        print(f"      {s['report_key']:<11} {s['score']:.2f}")
        print(wrap(f"“{s['evidence']}”", indent=18))
    if not diag["support"]:
        print(red("      no supporting reports"))
    pause(args)

    # Step 5 – verify
    status, checks = G.verify(out, lookup, proposed, diag)
    print(); print(bold("Step 5  VERIFY – deterministic checks"))
    for ch in checks:
        if ch.passed:
            mark = green("PASS  ")
        else:
            mark = red("BLOCK ") if ch.severity == "block" else amber("REVIEW")
        print(f"      {ch.id} {mark} {ch.name:<52} {dim(ch.detail)}")
    label = {"grounded": green("GROUNDED"), "needs_review": amber("NEEDS REVIEW"), "not_grounded": red("NOT GROUNDED")}[status]
    print(); print(bold("Result: ") + label + f"   {p} · {len(out['definition_ids'])} definitions · {len(out['supporting_reports'])} reports")
    cand = dict(candidate_id=cid, name=name, definition=definition, proposed_parent=proposed or "",
                expected_parent=None, expected_reports=[], manual=True)
    return dict(candidate=cand, output=out, diag=diag, status=status, checks=[ch.__dict__ for ch in checks])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.environ.get("GROUNDING_DB", "postgresql://grounding@localhost:5433/grounding"))
    ap.add_argument("--data", default=str(ROOT / "data"))
    ap.add_argument("--out", default=str(ROOT / "out"))
    ap.add_argument("--max-reports", type=int, help=f"most supporting reports per candidate (default {G.SETTINGS['max_reports']})")
    ap.add_argument("--min-support", type=int, help=f"G5 floor (default {G.SETTINGS['min_support']})")
    ap.add_argument("--model", help="sentence-transformers model name or local path (default: local LSA stand-in)")
    ap.add_argument("--name", help="candidate name (skips the prompt; runs once)")
    ap.add_argument("--definition", help="candidate definition")
    ap.add_argument("--proposed", help="parent proposed by discovery (optional, e.g. RE)")
    ap.add_argument("--step", action="store_true", help="pause after each step")
    args = ap.parse_args()
    if args.max_reports: G.SETTINGS["max_reports"] = args.max_reports
    if args.min_support: G.SETTINGS["min_support"] = args.min_support
    data, out_dir = Path(args.data), Path(args.out) / "interactive"
    out_dir.mkdir(parents=True, exist_ok=True)

    lj = lambda n, k: json.loads((data / n).read_text(encoding="utf-8"))[k]
    parents, defs = lj("icao_categories.json", "categories"), lj("industry_definitions.json", "definitions")
    reports = lj("sample_reports.json", "reports")
    cands = lj("candidates.json", "candidates") if (data / "candidates.json").exists() else []
    corpus = ([f"{p['name']}. {p['definition']}" for p in parents] + [f"{d['term']}. {d['text']}" for d in defs]
              + [r["narrative"] for r in reports] + [f"{c['name']}. {c['definition']}" for c in cands])
    emb = G.SentenceTransformerEmbedder(args.model) if args.model else G.LocalEmbedder(corpus)
    store = G.Store(args.db)
    store.load((ROOT / "db" / "schema.sql").read_text(), emb, parents, defs, reports, [])
    lookup = store.lookup()
    pmap = {p["code"]: p for p in parents}
    dmap = {d["id"]: d for d in defs}
    rmap = {r["report_key"]: r for r in reports}
    codes = [p["code"] for p in parents if p["in_scope"] and not p.get("co_code_only")]
    print(bold("Grounding – interactive mode"))
    print(f"Loaded {len(parents)} parents, {len(defs)} definitions, {len(reports)} reports from {data} (embedder {emb.name}).")
    print(dim("Allowed parents: " + ", ".join(codes)))

    results, n = [], 0
    while True:
        if args.name:
            name, definition, proposed = args.name, args.definition or args.name, (args.proposed or "").upper() or None
        else:
            print()
            name = ask(bold("Candidate name") + " (blank to quit): ")
            if not name:
                break
            definition = ask(bold("Definition") + " (one or two sentences; blank = use the name): ", name)
            proposed = (ask(bold("Proposed parent") + " (optional code, e.g. RE): ", "") or "").upper() or None
            if proposed and proposed not in pmap:
                print(amber(f"      {proposed} is not a known code – G8 will flag it."))
        n += 1
        cid = f"M{n:02d}"
        results.append(ground_typed(store, emb, lookup, pmap, dmap, rmap, name, definition, proposed, cid, args))
        summary = dict(mode="deterministic", candidates=len(results),
                       status={s: sum(r["status"] == s for r in results) for s in ("grounded", "needs_review", "not_grounded")})
        path = out_dir / "manual_results.json"
        json.dump(dict(run_id=dt.datetime.now().strftime("manual-%Y%m%d-%H%M%S"), mode="deterministic", embedder=emb.name,
                       dims=emb.dim, settings=G.SETTINGS, summary=summary, results=results, manual=True),
                  open(path, "w"), indent=1, default=str)
        print(dim(f"Saved {len(results)} candidate(s) to {path} – open it in the viewer with Load results."))
        if args.name:
            break


if __name__ == "__main__":
    main()
