"""Crossref via the public REST API."""

from __future__ import annotations

from ..http import get_json
from ..models import Paper, normalize_doi
from .base import Source, parse_year_range

_API = "https://api.crossref.org/works"


def _year(item: dict) -> int | None:
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (item.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return parts[0][0]
    return None


def _to_paper(item: dict) -> Paper:
    titles = item.get("title") or []
    authors = [
        " ".join(p for p in (a.get("given"), a.get("family")) if p)
        for a in (item.get("author") or [])
    ]
    pdf_url = None
    for link in item.get("link") or []:
        if link.get("content-type") == "application/pdf":
            pdf_url = link.get("URL")
            break
    containers = item.get("container-title") or []
    return Paper(
        source="crossref",
        paper_id=normalize_doi(item.get("DOI")) or item.get("DOI") or "",
        title=titles[0] if titles else "",
        authors=[a for a in authors if a],
        year=_year(item),
        doi=normalize_doi(item.get("DOI")),
        abstract=item.get("abstract"),
        url=item.get("URL"),
        pdf_url=pdf_url,
        venue=containers[0] if containers else None,
        citations=item.get("is-referenced-by-count"),
    )


class CrossrefSource(Source):
    name = "crossref"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        params = {"query": query, "rows": min(limit, 100)}
        lo, hi = parse_year_range(year)
        filt = []
        if lo is not None:
            filt.append(f"from-pub-date:{lo}-01-01")
        if hi is not None:
            filt.append(f"until-pub-date:{hi}-12-31")
        if filt:
            params["filter"] = ",".join(filt)
        data = get_json(_API, params=params)
        items = (data.get("message") or {}).get("items") or []
        return [_to_paper(i) for i in items][:limit]

    def fetch(self, paper_id: str) -> Paper | None:
        doi = normalize_doi(paper_id)
        if not doi:
            return None
        data = get_json(f"{_API}/{doi}")
        item = (data or {}).get("message")
        return _to_paper(item) if item else None
