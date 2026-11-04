"""
make_figures.py – figures for the grounding approach document, drawn from the trial outputs.

  python make_figures.py                 # approach, chain for C1, results matrix -> out/fig*.png
  python make_figures.py --candidate C5  # draw the grounding chain for another candidate
"""
import argparse
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = ["Calibri", "Carlito", "DejaVu Sans"]
ROOT = Path(__file__).parent
OUT = ROOT / "out"
INK = "#1B2A41"; NAVY = "#1F3864"; NAVY_L = "#E7ECF5"; SLATE = "#5B6B82"; LINE = "#D5DBE4"
TEAL = "#0E7C7B"; TEAL_L = "#E3F2F1"; GREEN = "#2E7D32"; GREEN_L = "#E8F3E8"; AMBER = "#C2620F"; AMBER_L = "#FBEEDF"
RED = "#B3261E"; RED_L = "#FBE9E7"


def box(ax, x, y, w, h, fc, ec, lw=1.2, r=0.18, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(ax, a, b, color=SLATE, lw=1.6, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>,head_length=7,head_width=4", color=color, lw=lw, ls=ls,
                                 connectionstyle=f"arc3,rad={rad}", zorder=3))


def wrap(t, n):
    return "\n".join(textwrap.wrap(t, n))


# ------------------------------------------------------------------ figure 1: the approach
def fig_approach(path):
    fig, ax = plt.subplots(figsize=(14, 7.2)); ax.set_xlim(0, 28); ax.set_ylim(0, 14.4); ax.axis("off")
    # candidate in
    box(ax, 0.3, 8.6, 3.6, 3.0, NAVY_L, NAVY)
    ax.text(2.1, 11.05, "Candidate\ncategories", ha="center", va="top", fontsize=12, fontweight="bold", color=INK)
    ax.text(2.1, 9.6, "from discovery\n(US 311617 stage 3)", ha="center", va="top", fontsize=9.5, color=SLATE)
    cols = [("1  RETRIEVE", TEAL, TEAL_L, "PostgreSQL + pgvector", [
                "Hybrid search: vector similarity", "+ full-text keywords", "",
                "Over 4 stores:", "• CICTT parent definitions", "• industry definitions", "• reports (D1b)", "• report sentences"]),
            ("2  CONSTRAIN", NAVY, NAVY_L, "choose only from closed sets", [
                "Parent: in-scope CICTT list", "Definitions: crosswalked (I-8)", "  to that parent", "Reports: already coded",
                "  to that parent", "One report per sibling", "", "Selector: rules, or LLM", "  answering in fixed JSON"]),
            ("3  VERIFY", GREEN, GREEN_L, "deterministic checks G1–G8", [
                "G1 parent allowed", "G2 definitions exist, crosswalked", "G3 reports exist, under parent", "G4 quotes word for word",
                "G5 enough support", "G6 parent agreement", "G7 clear winner", "G8 matches proposal"])]
    xs = [5.0, 11.2, 17.4]
    for x, (t, c, cl, sub, lines) in zip(xs, cols):
        box(ax, x, 4.6, 5.4, 8.2, cl, c, lw=1.6)
        box(ax, x, 11.5, 5.4, 1.3, c, c)
        ax.text(x + 0.3, 12.15, t, va="center", fontsize=13, fontweight="bold", color="white", zorder=4)
        ax.text(x + 0.3, 11.05, sub, va="center", fontsize=10, color=c, fontweight="bold", style="italic", zorder=4)
        for i, l in enumerate(lines):
            ax.text(x + 0.3, 10.35 - i * 0.68, l, va="center", fontsize=10, color=INK, zorder=4)
    arrow(ax, (3.9, 10.1), (5.0, 10.1), NAVY, 2)
    arrow(ax, (10.4, 10.1), (11.2, 10.1), NAVY, 2)
    arrow(ax, (16.6, 10.1), (17.4, 10.1), NAVY, 2)
    # outcomes
    outs = [(GREEN, GREEN_L, "Grounded", "to criteria card\nand review pack"), (AMBER, AMBER_L, "Needs review", "SME decides parent\nor co-code"),
            (RED, RED_L, "Not grounded", "agent loop or back\nto discovery")]
    for i, (c, cl, t, s) in enumerate(outs):
        y = 11.0 - i * 2.75
        box(ax, 23.6, y, 4.1, 2.1, cl, c, lw=1.5)
        ax.text(25.65, y + 1.4, t, ha="center", va="center", fontsize=12, fontweight="bold", color=c)
        ax.text(25.65, y + 0.62, s, ha="center", va="center", fontsize=9, color=INK, linespacing=1.15)
        arrow(ax, (22.8, 8.7), (23.6, y + 1.05), c, 1.4)
    # agent loop
    box(ax, 5.0, 0.4, 17.8, 3.3, "white", AMBER, lw=1.4)
    ax.text(5.3, 3.2, "AGENT WORKFLOW (escalation only, Should)", fontsize=11, fontweight="bold", color=AMBER, va="center")
    ax.text(5.3, 2.0, wrap("For candidates that fail: an agent with tools search_definitions · search_reports · read_report · "
                           "propose_split_or_merge · request_more_data re-plans the query, then sends its answer back through the same "
                           "VERIFY step. It never publishes; it only prepares a better candidate for SME review.", 118),
            fontsize=9.8, color=INK, va="center", linespacing=1.35)
    arrow(ax, (25.65, 5.5), (22.8, 2.0), AMBER, 1.4, "--", rad=-0.25)
    arrow(ax, (20.1, 3.7), (20.1, 4.6), AMBER, 1.4, "--")
    ax.text(20.3, 4.15, "re-verify", fontsize=8.5, color=AMBER, style="italic", va="center")
    ax.text(0.3, 7.6, "SME review stays\nthe final decision\n(AI proposes,\nSMEs approve)", fontsize=9.5, color=SLATE, style="italic", va="top")
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------ figure 2: one grounding chain
def fig_chain(path, res, cid, defs, parents, reports):
    r = next(x for x in res["results"] if x["candidate"]["candidate_id"] == cid)
    c, o = r["candidate"], r["output"]
    sup = o["supporting_reports"]
    n = len(sup)
    h = max(8.0, 1.55 * n + 2.4)
    fig, ax = plt.subplots(figsize=(14, h / 2)); ax.set_xlim(0, 28); ax.set_ylim(0, h); ax.axis("off")
    mid = h / 2
    # candidate
    box(ax, 0.3, mid - 1.9, 5.6, 3.8, NAVY_L, NAVY, lw=1.6)
    ax.text(0.6, mid + 1.5, f"CANDIDATE {cid}", fontsize=9.5, color=NAVY, fontweight="bold", va="center")
    ax.text(0.6, mid + 0.6, wrap(c["name"], 30), fontsize=12, color=INK, fontweight="bold", va="center")
    ax.text(0.6, mid - 1.05, wrap(c["definition"], 44), fontsize=8.4, color=SLATE, va="center")
    # parent
    p = parents[o["parent_code"]]
    box(ax, 7.0, mid - 1.3, 4.6, 2.6, NAVY, NAVY)
    ax.text(9.3, mid + 0.55, "ICAO PARENT (CICTT)", ha="center", fontsize=9, color="white", fontweight="bold", va="center")
    ax.text(9.3, mid - 0.3, f"{p['code']}  {p['name']}", ha="center", fontsize=12.5, color="white", fontweight="bold", va="center")
    arrow(ax, (5.9, mid), (7.0, mid), NAVY, 2)
    # definitions
    k = len(o["definition_ids"])
    for i, d in enumerate(o["definition_ids"]):
        y = mid + (k - 1) * 1.25 - i * 2.5 - 1.0
        box(ax, 12.8, y, 5.4, 2.0, TEAL_L, TEAL)
        term = defs[d]["term"] if len(defs[d]["term"]) <= 27 else defs[d]["term"][:26].rstrip(" –") + "…"
        ax.text(13.05, y + 1.55, f"{d}  {term}", fontsize=9.6, color=TEAL, fontweight="bold", va="center")
        ax.text(13.05, y + 0.95, wrap(defs[d]["source"], 52), fontsize=8.2, color=INK, va="center", style="italic")
        ax.text(13.05, y + 0.35, "crosswalk: " + ", ".join(defs[d]["parents"]), fontsize=8.2, color=SLATE, va="center")
        arrow(ax, (11.6, mid), (12.8, y + 1.0), TEAL, 1.4)
    ax.text(15.5, h - 0.35, "INDUSTRY DEFINITIONS", ha="center", fontsize=10, color=TEAL, fontweight="bold", va="center")
    # reports
    ax.text(23.6, h - 0.35, "SUPPORTING REPORTS (exact evidence)", ha="center", fontsize=10, color=GREEN, fontweight="bold", va="center")
    for i, s in enumerate(sup):
        y = h - 2.0 - i * 1.55
        box(ax, 19.4, y, 8.4, 1.35, GREEN_L, GREEN)
        rk = s["report_key"]
        ax.text(19.6, y + 1.05, f"{rk}  [{', '.join(reports[rk]['l1_codes'])}]", fontsize=8.8, color=GREEN, fontweight="bold", va="center")
        ax.text(19.6, y + 0.45, wrap("“" + s["evidence"] + "”", 74), fontsize=7.5, color=INK, va="center", style="italic")
        arrow(ax, (18.2, mid), (19.4, y + 0.67), GREEN, 1.0)
    status = r["status"].replace("_", " ").upper()
    col = {"GROUNDED": GREEN, "NEEDS REVIEW": AMBER, "NOT GROUNDED": RED}[status]
    ax.text(0.3, 0.35, f"Status: {status}   ·   checks " + " ".join(f"{ch['id']}{'✓' if ch['passed'] else '✗'}" for ch in r["checks"]),
            fontsize=10, color=col, fontweight="bold", va="center")
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------ figure 3: results matrix
def fig_matrix(path, res):
    rs = res["results"]
    ids = [ch["id"] for ch in rs[0]["checks"]]
    fig, ax = plt.subplots(figsize=(14, 0.62 * len(rs) + 1.6)); H = len(rs) + 1.6
    ax.set_xlim(0, 28); ax.set_ylim(0, H); ax.axis("off")
    cx = {"cand": 0.3, "parent": 9.3, "defs": 13.0, "reps": 14.3}
    x0 = 15.9; cw = 1.0
    for name, x in (("Candidate", cx["cand"]), ("Parent", cx["parent"]), ("Defs", cx["defs"]), ("Reports", cx["reps"])):
        ax.text(x, H - 0.55, name, fontsize=10, fontweight="bold", color=SLATE, va="center")
    for j, cid in enumerate(ids):
        ax.text(x0 + j * cw + cw / 2, H - 0.55, cid, ha="center", fontsize=10, fontweight="bold", color=SLATE, va="center")
    ax.text(x0 + len(ids) * cw + 0.3, H - 0.55, "Status", fontsize=10, fontweight="bold", color=SLATE, va="center")
    for i, r in enumerate(rs):
        y = H - 1.3 - i
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.1, y - 0.45), 27.8, 0.9, fc="#F5F7FA", ec="none", zorder=0))
        c, o = r["candidate"], r["output"]
        ax.text(cx["cand"], y, f"{c['candidate_id']}  {c['name'] if len(c['name']) <= 52 else c['name'][:51] + '…'}", fontsize=9.6, color=INK, va="center")
        changed = o["parent_code"] != c["proposed_parent"]
        ax.text(cx["parent"], y, o["parent_code"] + (f" (was {c['proposed_parent']})" if changed else ""), fontsize=9.2,
                color=AMBER if changed else INK, va="center", fontweight="bold" if changed else None)
        ax.text(cx["defs"] + 0.3, y, str(len(o["definition_ids"])), fontsize=9.6, color=INK, va="center", ha="center")
        ax.text(cx["reps"] + 0.45, y, str(len(o["supporting_reports"])), fontsize=9.6, color=INK, va="center", ha="center")
        for j, ch in enumerate(r["checks"]):
            fc = GREEN if ch["passed"] else (AMBER if ch["severity"] == "review" else RED)
            ax.add_patch(FancyBboxPatch((x0 + j * cw + 0.15, y - 0.3), cw - 0.3, 0.6, boxstyle="round,pad=0,rounding_size=0.12",
                                        fc=fc, ec="none", zorder=2))
            ax.text(x0 + j * cw + cw / 2, y, "✓" if ch["passed"] else "✗", ha="center", va="center", color="white", fontsize=10, fontweight="bold", zorder=3)
        st = r["status"].replace("_", " ")
        col = {"grounded": GREEN, "needs review": AMBER, "not grounded": RED}[st]
        ax.text(x0 + len(ids) * cw + 0.3, y, st.capitalize(), fontsize=10, color=col, fontweight="bold", va="center")
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", default="C1")
    ap.add_argument("--results", default=str(OUT / "grounding_results.json"))
    a = ap.parse_args()
    res = json.loads(Path(a.results).read_text())
    defs = {d["id"]: d for d in json.loads((ROOT / "data" / "industry_definitions.json").read_text())["definitions"]}
    parents = {p["code"]: p for p in json.loads((ROOT / "data" / "icao_categories.json").read_text())["categories"]}
    reports = {r["report_key"]: r for r in json.loads((ROOT / "data" / "sample_reports.json").read_text())["reports"]}
    fig_approach(OUT / "fig1_approach.png")
    fig_chain(OUT / f"fig2_chain_{a.candidate}.png", res, a.candidate, defs, parents, reports)
    fig_matrix(OUT / "fig3_results.png", res)
    print("figures in out/")


if __name__ == "__main__":
    main()
