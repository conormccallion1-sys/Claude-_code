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

## Setup (once)

The CLI is a Python package in this repository. Install its dependencies with uv:
uv sync --directory <REPO_PATH>

Optional environment variables (none are required for the default sweep):
- PAPER_SEARCH_EMAIL — your email; raises API rate limits (Crossref/OpenAlex/NCBI
  "polite pool") and is required by the `unpaywall` resolver.
- NCBI_API_KEY — higher PubMed/E-utilities rate limits.
- SEMANTIC_SCHOLAR_API_KEY — higher Semantic Scholar limits.
- CORE_API_KEY — required to use the `core` source.

## CLI Usage

All commands run via:
uv run --directory <REPO_PATH> paper-search <command> [args]

Replace <REPO_PATH> with the absolute path to your clone of this repository.

### Search
uv run --directory <REPO_PATH> paper-search search "<query>" -n <max_per_source> -s <sources> -y <year>
- -n: results per source (default: 5; use 20 during initial sweep)
- -s: comma-separated sources or "all" (default: the keyless, reliable set)
- -y: year filter — single year "2020" or range "2018-2024"; applied server-side
  where the API supports it, otherwise filtered client-side
- --no-dedup: keep every record instead of merging duplicates

Sources are queried concurrently. A source that errors (network, rate limit,
missing key) does not abort the sweep — its error is reported under "errors".

### Download PDF
uv run --directory <REPO_PATH> paper-search download <source> <paper_id> [-o ./downloads]
Resolves an open-access PDF for the record and saves it. `paper_id` is the id
from a search result for that source (a DOI works for most sources; an arXiv id
for arxiv). If the source has no direct PDF, it falls back to OpenAlex then
Unpaywall (set PAPER_SEARCH_EMAIL) to find an OA copy.

### Read (extract text)
uv run --directory <REPO_PATH> paper-search read <source> <paper_id> [-o ./downloads]
Downloads the PDF (as above) and prints extracted plain text to stdout.

### List sources
uv run --directory <REPO_PATH> paper-search sources [--json]

## Output
`search` returns a JSON envelope:
  { query, sources, year, total_raw, total_deduped, errors, results: [ ... ] }
Each result is a paper object: source, paper_id, title, authors, year, doi,
abstract, url, pdf_url, venue, citations. `download` returns JSON (path + bytes).
`read` returns plain text. Results are deduplicated by DOI (falling back to
title + first author + year), keeping the richest record across sources.

## Sources

Searchable (keyless, used in the default "all" sweep):
  arxiv, pubmed, pmc, europepmc, biorxiv, medrxiv, semantic, crossref, openalex,
  doaj, dblp, openaire, zenodo, hal
Searchable with a key: core (CORE_API_KEY)
Resolver only (no keyword search): unpaywall — DOI to open-access PDF, used by
  download/read; needs PAPER_SEARCH_EMAIL
Listed but not callable here (no usable public API without scraping/credentials):
  google_scholar, iacr, citeseerx, base, ssrn, ieee, acm
Run `paper-search sources` for the live status of each.

Note: biorxiv, medrxiv and pmc are served through the Europe PMC index (filtered
by publisher/source), so preprints and PMC open-access records are searchable
without a separate preprint-server API.

Priority sources for health psychology / chronic illness research:
  pubmed, pmc, europepmc, semantic, crossref, openalex, medrxiv, doaj

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

Measurement:
  "AddiQoL" OR "SF-36" OR "EQ-5D" OR "PHQ-9" OR "GAD-7"
  OR "patient-reported outcome" OR "PROM" OR "questionnaire" OR "Rasch"
  OR "psychometric" OR "validation"

Combine concepts with AND across blocks, OR within a block. Run each concept
block as its own sweep first, then run the AND-combined queries. Record every
query string you run so the search is reproducible.

---

### Phase 2 — Execute the search sweep

Run the initial broad sweep across all sources, then narrow.

1. Broad sweep — wide net, high recall:
   uv run --directory <REPO_PATH> paper-search search "<combined query>" -n 20 -s all

2. Targeted sweep — run the priority health-psychology sources with year filters:
   uv run --directory <REPO_PATH> paper-search search "<combined query>" -n 20 -s pubmed,pmc,europepmc,semantic,crossref,openalex -y 2010-2025

3. Save the raw JSON from every run. Each search returns JSON; redirect it to a
   per-query file (e.g. results/q01_broad.json) so nothing is lost between runs.

Log for each query: the exact query string, sources, -n, -y, date run, and the
hit count. This log is your PRISMA "identification" record.

---

### Phase 3 — Deduplicate

Merge all raw JSON into a single candidate set and remove duplicates:
- Primary key: DOI (normalise to lowercase, strip the https://doi.org/ prefix).
- Records without a DOI: dedupe on normalised title + first author + year.
- Keep the richest record when merging duplicates (prefer one with an abstract,
  PDF link, and citation count), but record every source it appeared in.

Report counts at each step: records identified, duplicates removed, records
remaining for screening.

---

### Phase 4 — Screen against criteria

Apply the Phase 0 inclusion/exclusion criteria — never criteria invented to fit
the results.

1. Title/abstract screen: mark each record include / exclude / unsure, with a
   one-line reason for every exclusion (e.g. "secondary adrenal insufficiency",
   "animal study", "no QoL outcome").
2. Full-text screen: download and read the PDFs of the survivors.
   uv run --directory <REPO_PATH> paper-search download <source> <paper_id> -o ./downloads
   uv run --directory <REPO_PATH> paper-search read <source> <paper_id> -o ./downloads
   Confirm each still meets every inclusion criterion. Log the exclusion reason
   for any dropped at full text.

Keep a running tally compatible with a PRISMA flow diagram:
identified -> deduplicated -> title/abstract screened -> full-text assessed -> included.

---

### Phase 5 — Snowball

Expand from the included set to catch what keyword search missed:
- Backward snowballing: scan the reference list of each included paper for
  relevant prior work.
- Forward snowballing: find papers that cite each included paper (use Semantic
  Scholar / OpenAlex citation data).
Feed new candidates back through Phase 3 (dedupe) and Phase 4 (screen). Repeat
until a snowball pass surfaces no new includes.

---

### Phase 6 — Extract and track gaps

For each included paper, extract into a structured table:
  citation, design, population/N, intervention/exposure, outcome measure(s),
  key findings, limitations.

Track gaps as you go:
- Concepts in the PICO with little or no coverage.
- Populations, designs, or outcome measures that are under-represented.
- Conflicting findings that need reconciling.

The gap list is the bridge from "what exists" to "what the review should argue."

---

### Phase 7 — Build the citation library

- Assign a stable citation key to each included paper.
- Store the canonical metadata (DOI, authors, year, title, venue) plus the local
  PDF path and the source it was retrieved from.
- Export to your reference manager (BibTeX/RIS) so it plugs into the write-up.
- Keep the query log, screening decisions, and PRISMA counts alongside the
  library so the whole review is reproducible and auditable.
