---
name: paper-search
description: Systematic literature review for academic research. Search 20+ sources,
  deduplicate by DOI, screen by inclusion/exclusion criteria, snowball references,
  and track gaps. Use when finding papers, running a literature review, or building
  a citation library.
---

# Paper Search — Systematic Literature Review

Search academic papers via the `paper-search` CLI and execute a full PRISMA-aligned
review pipeline.

## CLI Usage

All commands run via:
uv run --directory <REPO_PATH> paper-search <command> [args]

Replace <REPO_PATH> with the absolute path to your clone of this repository.

### Search
uv run --directory <REPO_PATH> paper-search search "<query>" -n <max_per_source> -s <sources> -y <year>
- -n: results per source (default: 5; use 20 during initial sweep)
- -s: comma-separated sources or "all" (default: all)
- -y: year filter for Semantic Scholar (e.g. "2020", "2018-2024")

### Download PDF
uv run --directory <REPO_PATH> paper-search download <source> <paper_id> [-o ./downloads]

### Read (extract text)
uv run --directory <REPO_PATH> paper-search read <source> <paper_id> [-o ./downloads]

### List sources
uv run --directory <REPO_PATH> paper-search sources

## Output
search and download return JSON. read returns plain text.

## Sources
arxiv, pubmed, biorxiv, medrxiv, google_scholar, iacr, semantic, crossref, openalex,
pmc, core, europepmc, dblp, openaire, citeseerx, doaj, base, zenodo, hal, ssrn, unpaywall
Optional (env vars): ieee (IEEE_API_KEY), acm (ACM_API_KEY)

Priority sources for health psychology / chronic illness research:
  pubmed, pmc, europepmc, semantic, crossref, openalex, google_scholar, medrxiv, doaj

Not in this CLI but essential — access via university institutional login:
  PsycINFO (psychology), Cochrane Library (systematic reviews / interventions),
  Embase (biomedical, strong on European literature), CINAHL (nursing and allied health)

---

## Systematic Literature Review Workflow

### Phase 0 — Define the review scope

Before any search, state and lock:
- Research question in PICO format:
    Population: who (e.g. adults with primary adrenal insufficiency / Addison's disease)
    Intervention/Exposure: what (e.g. glucocorticoid replacement regimen, diagnosis itself)
    Comparison: vs what, if applicable
    Outcome: what you're measuring (e.g. health-related QoL, fatigue, psychological wellbeing)
- Inclusion criteria: peer-reviewed only? Year range? Language? Study design (RCT,
  qualitative, cross-sectional, longitudinal)?
- Exclusion criteria: case reports only? Animal studies? Secondary adrenal insufficiency?
- Primary outcome measure(s): AddiQoL, SF-36, EQ-5D, PHQ-9, patient-reported outcomes

Lock these before the first search. Do not adjust criteria to match what you find.

---

### Phase 1 — Keyword matrix expansion

Generate the full term set for each concept before running a single search.

Condition:
  "Addison's disease" OR "primary adrenal insufficiency" OR "PAI"
  OR "primary hypoadrenalism" OR "autoimmune adrenalitis"
  OR "adrenocortical insufficiency"

Related physiology:
  "hydrocortisone" OR "glucocorticoid replacement" OR "fludrocortisone"
  OR "cortisol" OR "mineralocorticoid" OR "ACTH"

Quality of life:
  "quality of life" OR "QoL" OR "health-related quality of life" OR "HRQoL"
  OR "wellbeing" OR "well-being" OR "life satisfaction"

Health psychology:
  "health psychology" OR "psychological adjustment" OR "coping" OR "illness perception"
  OR "mental health" OR "anxiety" OR "depression" OR "fatigue" OR "patient experience"
  OR "self-management" OR "illness burden"

Measurement
