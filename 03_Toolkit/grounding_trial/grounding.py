"""
grounding.py – ground candidate taxonomy categories against ICAO/CICTT parents, industry definitions and reports.

Approach (see the grounding approach document):
  1. RETRIEVE  hybrid search in PostgreSQL + pgvector: vector similarity plus full-text keywords,
               over parent definitions, industry definitions, reports and report sentences.
  2. CONSTRAIN choose only from closed sets: the in-scope CICTT parent list, the industry
               definitions crosswalked to that parent, and reports already coded to that parent.
  3. VERIFY    deterministic checks on every link (ids exist, parent allowed, evidence quoted
               word for word, enough support, parent agreement). Failures go to SME review.

The same verify() is used whether the links come from the deterministic selector in this file or
from an LLM answering prompts/constrained_grounding.md.
"""
import json
import re
from dataclasses import dataclass, field

import numpy as np

# ------------------------------------------------------------------ settings (trial values)
SETTINGS = {
    "vector_weight": 0.6,        # hybrid score = 0.6 * vector cosine + 0.4 * keyword rank (normalised)
    "pool_size": 10,             # reports retrieved without a parent filter, used to vote on the parent
    "relative_cutoff": 0.4,      # keep reports / definitions scoring at least 40% of the best match
    "min_score": 0.15,           # ... and never below this floor
    "parent_def_weight": 0.3,    # parent score = 0.3 * definition fit + 0.7 * report vote
    "parent_margin": 0.10,       # if the runner-up parent is closer than this, flag for SME review
    "max_definitions": 3,
    "max_reports": 8,
    "min_support": 3,            # trial value; US 311617 uses a 10-report floor in production
    "min_parent_agreement": 0.6, # share of the evidence pool that sits under the chosen parent
}
STOP = set("""a an the and or of to in on at for from by with without is are was were be been it its this that
than then as into over under after before during other such any all not no can may per their there which while
""".split())


# ------------------------------------------------------------------ embeddings
class LocalEmbedder:
    """Stand-in for an aviation embedding model (e.g. SafeAeroBERT) when no model can be downloaded:
    TF-IDF over words and word pairs, reduced to dense vectors with truncated SVD (LSA)."""
    name = "local-lsa"

    def __init__(self, corpus, dim=64, seed=7):
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english", min_df=1)
        X = self.vec.fit_transform(corpus)
        self.dim = min(dim, X.shape[0] - 1, X.shape[1] - 1)
        self.svd = TruncatedSVD(n_components=self.dim, random_state=seed).fit(X)

    def encode(self, texts):
        Z = self.svd.transform(self.vec.transform(texts))
        Z /= np.linalg.norm(Z, axis=1, keepdims=True) + 1e-12
        return Z.astype(np.float32)


class SentenceTransformerEmbedder:
    """Production option: any sentence-transformers model available inside the approved environment."""
    def __init__(self, model_name):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        self.name = model_name
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode(self, texts):
        return np.asarray(self.model.encode(list(texts), normalize_embeddings=True), dtype=np.float32)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def keyword_query(text):
    """OR-query of content words for PostgreSQL to_tsquery."""
    words = [w for w in re.findall(r"[a-z][a-z\-]+", text.lower()) if w not in STOP and len(w) > 2]
    words = sorted(set(w.replace("-", "") for w in words))
    return " | ".join(words) if words else "none"


# ------------------------------------------------------------------ store (PostgreSQL + pgvector)
class Store:
    def __init__(self, dsn):
        import psycopg
        from pgvector.psycopg import register_vector
        self.conn = psycopg.connect(dsn, autocommit=True)
        self.conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(self.conn)

    def q(self, sql, params=()):
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if cur.description else []

    def load(self, schema_sql, emb, parents, definitions, reports, candidates, version="trial"):
        self.conn.execute(schema_sql.replace("{DIM}", str(emb.dim)))
        pv = emb.encode([f"{p['name']}. {p['definition']}" for p in parents])
        for p, v in zip(parents, pv):
            self.q("INSERT INTO icao_category VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   (p["code"], p["name"], p["definition"], p["in_scope"], p.get("co_code_only", False), version, v))
        dv = emb.encode([f"{d['term']}. {d['text']}" for d in definitions])
        for d, v in zip(definitions, dv):
            self.q("INSERT INTO industry_definition (def_id, source, term, body, parents, version, embedding) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   (d["id"], d["source"], d["term"], d["text"], d["parents"], version, v))
        rv = emb.encode([r["narrative"] for r in reports])
        for r, v in zip(reports, rv):
            self.q("INSERT INTO report (report_key, source_id, phase, l1_codes, source_codes, narrative, embedding) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   (r["report_key"], r["source_id"], r["phase"], r["l1_codes"], r["source_codes"], r["narrative"], v))
            ss = sentences(r["narrative"])
            for i, (s, sv) in enumerate(zip(ss, emb.encode(ss))):
                self.q("INSERT INTO report_sentence VALUES (%s,%s,%s,%s)", (r["report_key"], i, s, sv))
        cv = emb.encode([f"{c['name']}. {c['definition']}" for c in candidates]) if candidates else []
        for c, v in zip(candidates, cv):
            self.q("INSERT INTO candidate VALUES (%s,%s,%s,%s,%s)", (c["candidate_id"], c["name"], c["definition"], c["proposed_parent"], v))

    # --- retrieval primitives -------------------------------------------------
    def parent_fit(self, vec):
        return self.q("""SELECT code, name, definition, 1 - (embedding <=> %s) AS cos
                         FROM icao_category WHERE in_scope AND NOT co_code_only ORDER BY embedding <=> %s""", (vec, vec))

    def reports_hybrid(self, vec, text, parent=None, limit=10):
        w = SETTINGS["vector_weight"]
        rows = self.q(f"""
            WITH s AS (
              SELECT report_key, l1_codes, narrative,
                     1 - (embedding <=> %s) AS cos,
                     ts_rank_cd(tsv, to_tsquery('english', %s)) AS kw
              FROM report {'WHERE l1_codes @> %s' if parent else ''})
            SELECT report_key, l1_codes, narrative, cos, kw,
                   {w} * cos + {1 - w} * (kw / NULLIF(max(kw) OVER (), 0)) AS score
            FROM s ORDER BY score DESC NULLS LAST LIMIT %s""",
            (vec, keyword_query(text), [parent], limit) if parent else (vec, keyword_query(text), limit))
        return [dict(report_key=r[0], l1_codes=r[1], narrative=r[2], cos=float(r[3]), kw=float(r[4]),
                     score=float(r[5]) if r[5] is not None else float(r[3]) * w) for r in rows]

    def definitions_for(self, vec, text, parent, limit=5):
        w = SETTINGS["vector_weight"]
        rows = self.q(f"""
            WITH s AS (
              SELECT def_id, source, term, body, parents, 1 - (embedding <=> %s) AS cos,
                     ts_rank_cd(tsv, to_tsquery('english', %s)) AS kw
              FROM industry_definition WHERE parents @> %s)
            SELECT def_id, source, term, body, parents, cos,
                   {w} * cos + {1 - w} * coalesce(kw / NULLIF(max(kw) OVER (), 0), 0) AS score
            FROM s ORDER BY score DESC LIMIT %s""", (vec, keyword_query(text), [parent], limit))
        return [dict(def_id=r[0], source=r[1], term=r[2], body=r[3], parents=r[4], cos=float(r[5]), score=float(r[6])) for r in rows]

    def best_sentence(self, vec, report_key, text=""):
        """Evidence sentence: vector similarity plus stemmed keyword rank of the sentence (PostgreSQL full text)."""
        rows = self.q("""SELECT sentence, 1 - (embedding <=> %s),
                                ts_rank_cd(to_tsvector('english', sentence), to_tsquery('english', %s))
                         FROM report_sentence WHERE report_key = %s ORDER BY seq""", (vec, keyword_query(text), report_key))
        if not rows:
            return "", 0.0
        top_kw = max(float(r[2]) for r in rows) or 1.0
        best = max(rows, key=lambda r: 0.5 * float(r[1]) + 0.5 * float(r[2]) / top_kw)
        return best[0], float(best[1])

    def candidate(self, cid):
        r = self.q("SELECT candidate_id, name, definition, proposed_parent, embedding FROM candidate WHERE candidate_id = %s", (cid,))[0]
        return dict(candidate_id=r[0], name=r[1], definition=r[2], proposed_parent=r[3], embedding=r[4])

    def lookup(self):
        """Closed sets the verifier checks against."""
        parents = {r[0]: dict(in_scope=r[1], co_code_only=r[2]) for r in self.q("SELECT code, in_scope, co_code_only FROM icao_category")}
        defs = {r[0]: r[1] for r in self.q("SELECT def_id, parents FROM industry_definition")}
        reps = {r[0]: dict(l1=r[1], text=r[2]) for r in self.q("SELECT report_key, l1_codes, narrative FROM report")}
        return parents, defs, reps


# ------------------------------------------------------------------ deterministic constrained selection
def relevant(items, key="score"):
    """Keep items within the relative cut-off of the best one, and above the floor."""
    if not items:
        return []
    top = max(i[key] for i in items)
    cut = max(SETTINGS["min_score"], SETTINGS["relative_cutoff"] * top)
    return [i for i in items if i[key] >= cut]


def ground_candidate(store, cid, mode="hybrid"):
    """Returns a grounding output (same shape as the LLM JSON) plus diagnostics."""
    c = store.candidate(cid)
    vec, text = c["embedding"], f"{c['name']}. {c['definition']}"

    # 1. parent: definition fit + vote of the reports that best match the candidate
    fits = store.parent_fit(vec)
    codes = [f[0] for f in fits]
    fit_n = {f[0]: max(0.0, float(f[3])) for f in fits}
    pool = relevant(store.reports_hybrid(vec, text, limit=SETTINGS["pool_size"]))
    tot = sum(p["score"] for p in pool) or 1.0
    vote = {code: sum(p["score"] for p in pool if code in p["l1_codes"]) / tot for code in codes}
    wd = SETTINGS["parent_def_weight"]
    if mode == "definition_only":
        score = fit_n
    elif mode == "vote_only":
        score = vote
    else:
        score = {k: wd * fit_n[k] + (1 - wd) * vote[k] for k in codes}
    ranked = sorted(codes, key=lambda k: -score[k])
    parent, runner = ranked[0], ranked[1]

    # 2. industry definitions crosswalked to that parent
    defs = relevant(store.definitions_for(vec, text, parent))[:SETTINGS["max_definitions"]]

    # 3. supporting reports already coded to that parent, with an exact evidence sentence
    support = []
    for r in relevant(store.reports_hybrid(vec, text, parent=parent, limit=SETTINGS["max_reports"] * 2)):
        if len(support) >= SETTINGS["max_reports"]:
            break
        sent, s_cos = store.best_sentence(vec, r["report_key"], text)
        support.append(dict(report_key=r["report_key"], evidence=sent, score=round(r["score"], 3)))

    out = dict(candidate_id=cid, parent_code=parent,
               definition_ids=[d["def_id"] for d in defs],
               supporting_reports=[dict(report_key=s["report_key"], evidence=s["evidence"]) for s in support],
               concerns="")
    co = [k for k in ranked[1:] if vote[k] >= SETTINGS["min_parent_agreement"]]
    diag = dict(candidate=c["name"], proposed_parent=c["proposed_parent"], co_codes=co, parent_scores={k: round(score[k], 3) for k in ranked[:4]},
                runner_up=runner, margin=round(score[parent] - score[runner], 3), parent_agreement=round(vote[parent], 3),
                parent_definition_rank=codes.index(parent) + 1, definitions=defs, support=support,
                pool=[dict(report_key=p["report_key"], l1=p["l1_codes"], score=round(p["score"], 3)) for p in pool])
    return out, diag


def resolve_siblings(grounded):
    """grounded: list of (output, diag). A report may support only one sibling (same parent):
    it stays with the candidate it matches best and is removed from the others."""
    best = {}
    for out, diag in grounded:
        for s in diag["support"]:
            k = (out["parent_code"], s["report_key"])
            if k not in best or s["score"] > best[k][1]:
                best[k] = (out["candidate_id"], s["score"])
    for out, diag in grounded:
        keep, moved = [], []
        for s in diag["support"]:
            owner = best[(out["parent_code"], s["report_key"])][0]
            (keep if owner == out["candidate_id"] else moved).append(s if owner == out["candidate_id"] else (s["report_key"], owner))
        diag["support"] = keep
        diag["moved_to_sibling"] = moved
        out["supporting_reports"] = [dict(report_key=s["report_key"], evidence=s["evidence"]) for s in keep]
    return grounded


# ------------------------------------------------------------------ verifier (used for deterministic and LLM output)
@dataclass
class Check:
    id: str
    name: str
    passed: bool
    detail: str
    severity: str = "block"       # block -> not grounded; review -> needs SME review


def verify(output, lookup, proposed_parent=None, diag=None):
    parents, defs, reps = lookup
    p = output.get("parent_code")
    checks = []
    ok_parent = p in parents and parents[p]["in_scope"] and not parents[p]["co_code_only"]
    checks.append(Check("G1", "Parent is an allowed CICTT category", ok_parent, f"parent = {p}"))

    bad_defs = [d for d in output.get("definition_ids", []) if d not in defs]
    wrong_x = [d for d in output.get("definition_ids", []) if d in defs and p not in defs[d]]
    n_defs = len(output.get("definition_ids", [])) - len(bad_defs) - len(wrong_x)
    checks.append(Check("G2", "Definitions exist and are crosswalked to the parent", not bad_defs and not wrong_x and n_defs >= 1,
                        f"{n_defs} valid" + (f"; unknown {bad_defs}" if bad_defs else "") + (f"; not crosswalked to {p}: {wrong_x}" if wrong_x else "")))

    sup = output.get("supporting_reports", [])
    bad_keys = [s["report_key"] for s in sup if s["report_key"] not in reps]
    not_quoted = [s["report_key"] for s in sup if s["report_key"] in reps and s["evidence"] not in reps[s["report_key"]]["text"]]
    off_parent = [s["report_key"] for s in sup if s["report_key"] in reps and p not in reps[s["report_key"]]["l1"]]
    checks.append(Check("G3", "Every report exists and is coded to the parent", not bad_keys and not off_parent,
                        "ok" if not bad_keys and not off_parent else f"unknown {bad_keys}; not under {p}: {off_parent}"))
    checks.append(Check("G4", "Evidence is quoted word for word", not not_quoted,
                        "all quotes found in the report text" if not not_quoted else f"not found in report: {not_quoted}"))
    n_ok = len(sup) - len(set(bad_keys + not_quoted + off_parent))
    checks.append(Check("G5", f"At least {SETTINGS['min_support']} supporting reports", n_ok >= SETTINGS["min_support"], f"{n_ok} valid"))

    if diag is not None:
        agree = diag["parent_agreement"]
        checks.append(Check("G6", "Evidence sits under the parent (agreement)", agree >= SETTINGS["min_parent_agreement"],
                            f"{agree:.0%} of the closest reports are coded {p}", "review"))
        checks.append(Check("G7", "Clear winner among parents", diag["margin"] >= SETTINGS["parent_margin"],
                            f"margin {diag['margin']:.2f} over {diag['runner_up']}", "review"))
    if proposed_parent:
        checks.append(Check("G8", "Matches the parent proposed by discovery", p == proposed_parent,
                            f"proposed {proposed_parent}, grounded {p}", "review"))

    if any(not c.passed and c.severity == "block" for c in checks):
        status = "not_grounded"
    elif any(not c.passed for c in checks):
        status = "needs_review"
    else:
        status = "grounded"
    return status, checks


def build_prompt(template, store, cid, k_reports=10):
    """Fill prompts/constrained_grounding.md with the retrieved context for an LLM."""
    c = store.candidate(cid)
    vec, text = c["embedding"], f"{c['name']}. {c['definition']}"
    parents = store.parent_fit(vec)
    pool = store.reports_hybrid(vec, text, limit=k_reports)
    defs = store.q("""SELECT def_id, term, body, parents FROM industry_definition ORDER BY embedding <=> %s LIMIT 8""", (vec,))
    fill = {
        "CANDIDATE_ID": cid, "CANDIDATE_NAME": c["name"], "CANDIDATE_DEFINITION": c["definition"],
        "PROPOSED_PARENT": c["proposed_parent"],
        "PARENT_LIST": "\n".join(f"- {p[0]} ({p[1]}): {p[2]}" for p in parents),
        "DEFINITION_LIST": "\n".join(f"- {d[0]} [{', '.join(d[3])}] {d[1]}: {d[2]}" for d in defs),
        "REPORT_LIST": "\n".join(f"- {r['report_key']} [{', '.join(r['l1_codes'])}]: {r['narrative']}" for r in pool),
    }
    for k, v in fill.items():
        template = template.replace("{" + k + "}", v)
    return template
