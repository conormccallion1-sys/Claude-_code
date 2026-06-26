"""PubMed via NCBI E-utilities (esearch + esummary)."""

from __future__ import annotations

import os

from ..http import get_json
from ..models import Paper, normalize_doi
from .base import Source, parse_year_range

_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _common_params() -> dict:
    params = {"db": "pubmed", "retmode": "json", "tool": "paper-search"}
    if os.environ.get("NCBI_API_KEY"):
        params["api_key"] = os.environ["NCBI_API_KEY"]
    email = os.environ.get("PAPER_SEARCH_EMAIL")
    if email:
        params["email"] = email
    return params


def _summary_to_paper(uid: str, doc: dict) -> Paper:
    doi = None
    for aid in doc.get("articleids") or []:
        if aid.get("idtype") == "doi":
            doi = normalize_doi(aid.get("value"))
            break
    year = None
    pubdate = doc.get("pubdate") or ""
    if pubdate[:4].isdigit():
        year = int(pubdate[:4])
    authors = [a.get("name", "") for a in (doc.get("authors") or []) if a.get("name")]
    return Paper(
        source="pubmed",
        paper_id=doi or uid,
        title=doc.get("title") or "",
        authors=authors,
        year=year,
        doi=doi,
        abstract=None,  # esummary omits abstracts; use europepmc/efetch for full text
        url=f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
        pdf_url=None,
        venue=doc.get("fulljournalname") or doc.get("source"),
    )


class PubMedSource(Source):
    name = "pubmed"

    def _term(self, query: str, year: str | None) -> str:
        lo, hi = parse_year_range(year)
        if lo is not None or hi is not None:
            lo = lo or 1800
            hi = hi or 3000
            return f"({query}) AND ({lo}:{hi}[dp])"
        return query

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        params = _common_params()
        params.update({"term": self._term(query, year), "retmax": min(limit, 100), "sort": "relevance"})
        res = get_json(f"{_BASE}/esearch.fcgi", params=params)
        ids = (res.get("esearchresult") or {}).get("idlist") or []
        if not ids:
            return []
        sparams = _common_params()
        sparams["id"] = ",".join(ids)
        summ = get_json(f"{_BASE}/esummary.fcgi", params=sparams)
        result = summ.get("result") or {}
        papers = []
        for uid in result.get("uids", []):
            doc = result.get(uid)
            if doc:
                papers.append(_summary_to_paper(uid, doc))
        return papers[:limit]

    def fetch(self, paper_id: str) -> Paper | None:
        uid = paper_id.strip()
        sparams = _common_params()
        sparams["id"] = uid
        summ = get_json(f"{_BASE}/esummary.fcgi", params=sparams)
        result = summ.get("result") or {}
        doc = result.get(uid)
        return _summary_to_paper(uid, doc) if doc else None
