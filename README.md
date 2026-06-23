# Claude-_code

A Claude Code **skill** for searching and reading academic papers.

## What's here

- [`SKILL.md`](./SKILL.md) — the `paper-search` skill definition. It tells Claude
  how to find papers, fetch full text, and gather citations using the connected
  research MCP servers (Consensus, PubMed, bioRxiv/medRxiv, Scholar Gateway, Exa).

## How it works

This skill has **no local CLI or package to install**. Paper search is provided
by MCP servers that run in the Claude Code session, covering Semantic Scholar,
PubMed, Scopus, arXiv, and bioRxiv/medRxiv. `SKILL.md` documents which MCP tool
to use for each job (search, read full text, find related work).

> Note: an earlier version of this skill referenced a `paper-search` CLI run via
> `uv run`. No such package existed in the repo, and sandboxed sessions block
> direct network access to academic APIs — so the skill now uses MCP tools, which
> already cover the same sources without needing egress. See the bottom of
> `SKILL.md` for details.

## Usage

Just ask Claude to find papers, e.g.:

- "Find recent papers on CRISPR off-target effects."
- "Search PubMed for mRNA vaccine immunogenicity studies from 2023."
- "Get the full text of PMID 42327745."
