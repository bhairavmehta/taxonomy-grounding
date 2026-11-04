"""
combine_datasets.py – merge several grounding datasets (data folders) into one.

  python tools/combine_datasets.py                                   # data/ + data_sample_b/ -> data_combined/
  python tools/combine_datasets.py --inputs data data_sample_b data_sample_c --out data_all

Parents and definitions are merged by code / id (the first folder wins if the text differs, and a warning is printed).
Reports and candidates are appended; duplicate keys or ids stop the merge.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Candidates from different batches that describe the same events (discovery would merge these).
# Used to score "counting overlaps": a report linked to an overlapping candidate is not counted as an error.
OVERLAPS = {"C1": ["B02"], "C2": ["B01", "B27"], "C3": ["B04"], "C4": ["B26"], "C5": ["B08"],
            "C7": ["B15"], "C8": ["B14"], "C9": ["B22"]}
FILES = [("icao_categories.json", "categories", "code"), ("industry_definitions.json", "definitions", "id"),
         ("sample_reports.json", "reports", "report_key"), ("candidates.json", "candidates", "candidate_id")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", default=["data", "data_sample_b"])
    ap.add_argument("--out", default="data_combined")
    a = ap.parse_args()
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    for fname, key, idf in FILES:
        merged, seen = [], {}
        for folder in a.inputs:
            for item in json.loads((ROOT / folder / fname).read_text(encoding="utf-8"))[key]:
                k = item[idf]
                if k in seen:
                    if key in ("reports", "candidates"):
                        raise SystemExit(f"duplicate {idf} {k} in {folder}/{fname}")
                    if {x: v for x, v in item.items() if x != "parents"} != {x: v for x, v in seen[k].items() if x != "parents"}:
                        print(f"  note: {k} differs in {folder}/{fname}; keeping the first version")
                    continue
                seen[k] = item
                merged.append(item)
        if key == "candidates":
            ov = {}
            for c, others in OVERLAPS.items():
                for o in others:
                    ov.setdefault(c, set()).add(o); ov.setdefault(o, set()).add(c)
            ids = {m["candidate_id"] for m in merged}
            for m in merged:
                m["overlaps"] = sorted(x for x in ov.get(m["candidate_id"], ()) if x in ids)
        note = f"Combined from {', '.join(a.inputs)}. Reports are SYNTHETIC (written or template-generated for the trial), not real events."
        json.dump({"_note": note, key: merged}, open(out / fname, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"  {fname:<26} {len(merged):>4} {key}")
    print(f"Combined -> {out}")


if __name__ == "__main__":
    main()
