PIPELINE STEP: grounding

You are grounding ONE candidate safety-risk category. Use ONLY the context below. Do not use outside knowledge.

CANDIDATE
id: {CANDIDATE_ID}
name: {CANDIDATE_NAME}
definition: {CANDIDATE_DEFINITION}
proposed parent (from discovery, may be wrong): {PROPOSED_PARENT}

ALLOWED PARENT CATEGORIES (CICTT Level 1 – choose exactly one code from this list)
{PARENT_LIST}

RETRIEVED INDUSTRY DEFINITIONS (choose only from these ids)
{DEFINITION_LIST}

RETRIEVED REPORTS (choose only from these keys; quote evidence word for word)
{REPORT_LIST}

TASK
1. Choose the parent_code that best fits the candidate. It must be one of the allowed codes. If none fits, use "NONE".
2. List the definition_ids that the candidate's meaning draws on (0–3). Each must list the chosen parent in its crosswalk.
3. List supporting reports (up to 8). For each, give the report_key and an evidence quote copied exactly from that report's text. Only include reports that clearly match the candidate definition.
4. If the evidence is weak or the proposed parent looks wrong, say so in "concerns".

Reply with JSON only, matching this schema: grounding_output.schema.json
