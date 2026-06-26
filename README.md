# paper-search

A command-line tool for systematic literature review: search 15+ academic
sources at once, deduplicate by DOI, and download/read open-access PDFs.

The agent-facing workflow (PRISMA phases, keyword-matrix guidance, screening)
lives in [`SKILL.md`](./SKILL.md).

## Install

```sh
uv sync
```

## Quick start

```sh
# search across the default keyless sources
uv run paper-search search "Addison's disease quality of life" -n 10 -y 2015-2025

# narrow to specific sources
uv run paper-search search "hydrocortisone HRQoL" -s pubmed,europepmc,openalex

# list sources and their status
uv run paper-search sources

# download / read a PDF (id is from a search result; a DOI works for most sources)
uv run paper-search download openalex 10.1234/example -o ./downloads
uv run paper-search read arxiv 2401.01234
```

`search` and `download` print JSON; `read` prints extracted text. Results are
deduplicated by DOI (falling back to title + first author + year), keeping the
richest record found across sources.

## Optional environment variables

None are required for the default sweep.

| Variable | Effect |
| --- | --- |
| `PAPER_SEARCH_EMAIL` | Polite-pool rate limits (Crossref/OpenAlex/NCBI); required by `unpaywall` |
| `NCBI_API_KEY` | Higher PubMed / E-utilities limits |
| `SEMANTIC_SCHOLAR_API_KEY` | Higher Semantic Scholar limits |
| `CORE_API_KEY` | Enables the `core` source |

## Tests

```sh
uv run --with pytest pytest tests/
```

The tests are offline (HTTP is mocked), so they pass without network egress to
the academic APIs.
