"""Semantic Scholar via the public Graph API."""

from __future__ import annotations

import os

from ..http import get_json
from ..models import Paper, normalize_doi
from .base import Source

_API = "https://api.semanticscholar.org/graph/v1/paper"
_FIELDS = (
    "title,abstract,year,authors,externalIds,venue,citationCount,"
    "openAccessPdf,url"
)


def _headers() -> dict:
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    return {"x-api-key": key} if key else {}


def _to_paper(p: dict) -> Paper:
    ext = p.get("externalIds") or {}
    oa = p.get("openAccessPdf") or {}
    return Paper(
        source="semantic",
        paper_id=p.get("paperId") or "",
        title=p.get("title") or "",
        authors=[a.get("name", "") for a in (p.get("authors") or [])],
        year=p.get("year"),
        doi=normalize_doi(ext.get("DOI")),
        abstract=p.get("abstract"),
        url=p.get("url"),
        pdf_url=oa.get("url"),
        venue=p.get("venue"),
        citations=p.get("citationCount"),
    )


class SemanticScholarSource(Source):
    name = "semantic"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        params = {"query": query, "limit": min(limit, 100), "fields": _FIELDS}
        if year:
            params["year"] = year  # API accepts "2020" or "2018-2024"
        data = get_json(f"{_API}/search", params=params, headers=_headers())
        return [_to_paper(p) for p in (data.get("data") or [])][:limit]

    def fetch(self, paper_id: str) -> Paper | None:
        ident = paper_id.strip()
        doi = normalize_doi(ident)
        key = f"DOI:{doi}" if doi else ident
        data = get_json(f"{_API}/{key}", params={"fields": _FIELDS}, headers=_headers())
        return _to_paper(data) if data else None
