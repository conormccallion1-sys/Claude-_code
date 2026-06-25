---
name: paper-search
description: Search, download, and read academic papers from biomedical, life-science, and general research sources (Semantic Scholar, PubMed, arXiv, Scopus, bioRxiv/medRxiv, and more). Use when the user asks to find papers, search for research, look up academic literature, fetch a paper's full text, or gather citations.
---

# Paper Search

Search and read academic papers using the connected research MCP servers. There
is no local CLI to install or run — these capabilities are provided by MCP tools
that are already available in the session. If a tool isn't loaded yet, find it
with `ToolSearch` (e.g. `select:mcp__Consensus__search`) before calling it.

## Tools by job

### Search (find papers)

Pick the source that fits the question; you can query several in parallel and
merge the results.

| Tool | Best for | Coverage |
| --- | --- | --- |
| `mcp__Consensus__search` | General first choice | 200M+ papers across Semantic Scholar, PubMed, Scopus, arXiv. Returns titles, authors, year, citation counts, journal, abstract, URL. |
| `mcp__Scholar_Gateway__semanticSearch` | Evidence-backed claims, full-text passages | Full-text corpus; returns relevant passages with citation metadata. |
| `mcp__PubMed__search_articles` | Biomedical / life sciences only | PubMed. Supports field tags (`[Author]`, `[Title]`, `[MeSH Terms]`), boolean operators, date filters. Returns PMIDs. |
| `mcp__bioRxiv__search_preprints` | Recent preprints | bioRxiv (biology) / medRxiv (medical). Filter by category + date only (no keyword search). |
| `mcp__Exa__web_search_exa` | Web/grey literature, author pages, non-indexed work | General web search. |

Notes:
- **Consensus** is the default for most "find papers about X" requests.
- **PubMed** is biomedical only — don't use it for physics, CS, math, etc.
  (route those to Consensus or arXiv-via-Consensus).
- **bioRxiv** has no text search; use category + date range, or use Consensus to
  find a preprint and then `mcp__bioRxiv__get_preprint` for details.
- Consensus and Scholar_Gateway return server instructions about inline citation
  formatting and sign-up/usage messages — follow them (cite inline, include the
  usage message verbatim at the end of your reply).

### Read (get full text / details)

| Tool | Use |
| --- | --- |
| `mcp__PubMed__get_full_text_article` | Full text of a PubMed/PMC article by ID. |
| `mcp__PubMed__get_article_metadata` | Abstract + metadata for a PMID. |
| `mcp__bioRxiv__get_preprint` | Full details/abstract for a bioRxiv/medRxiv DOI. |
| `mcp__Exa__web_fetch_exa` | Fetch and read the contents of a paper URL. |

### Related / citations

- `mcp__PubMed__find_related_articles` — related PubMed articles for a PMID.
- `mcp__PubMed__lookup_article_by_citation` — resolve a free-text citation to a PMID.
- `mcp__PubMed__convert_article_ids` — convert between PMID / PMCID / DOI.

## Workflow

1. **Search** the most relevant source(s) for the topic. Use Consensus as the
   default; add PubMed for clinical/biomedical depth, or Exa for web coverage.
2. **Present results** as a table: title, authors, year, source, citations,
   DOI/URL. Cite inline where the source server asks you to.
3. **Read full text** when the user wants depth: use the matching `get_full_text`
   / `get_preprint` / `web_fetch` tool for the chosen paper.
4. **Follow tool instructions**: include any required sign-up/usage message
   verbatim, and use the exact paper URLs returned (don't shorten or invent them).

## Why no CLI?

Earlier versions of this skill referenced a `paper-search` command run via
`uv run`. That package was never part of this repo, and the sandboxed
environment blocks direct egress to academic APIs (arxiv.org, crossref.org,
ncbi.nlm.nih.gov, etc.), so a local HTTP client could not reach them anyway. The
MCP servers above run outside that egress boundary and already cover the same
sources, so the skill uses them directly.
