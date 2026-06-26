"""OpenAlex via its public REST API. Also used to resolve OA PDFs by DOI."""

from __future__ import annotations

import os

from ..http import get_json
from ..models import Paper, normalize_doi
from .base import Source, parse_year_range

_API = "https://api.openalex.org/works"


def _reconstruct_abstract(inv_index: dict | None) -> str | None:
    if not inv_index:
        return None
    positions: list[tuple[int, str]] = []
    for word, idxs in inv_index.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions) or None


def _to_paper(w: dict) -> Paper:
    doi = normalize_doi(w.get("doi"))
    oa = (w.get("best_oa_location") or w.get("primary_location") or {}) or {}
    pdf_url = oa.get("pdf_url")
    host = (w.get("primary_location") or {}).get("source") or {}
    return Paper(
        source="openalex",
        paper_id=(w.get("id") or "").rsplit("/", 1)[-1],
        title=w.get("title") or w.get("display_name") or "",
        authors=[
            (a.get("author") or {}).get("display_name", "")
            for a in (w.get("authorships") or [])
        ],
        year=w.get("publication_year"),
        doi=doi,
        abstract=_reconstruct_abstract(w.get("abstract_inverted_index")),
        url=w.get("doi") or w.get("id"),
        pdf_url=pdf_url,
        venue=host.get("display_name"),
        citations=w.get("cited_by_count"),
    )


def _mailto() -> dict:
    email = os.environ.get("PAPER_SEARCH_EMAIL")
    return {"mailto": email} if email else {}


class OpenAlexSource(Source):
    name = "openalex"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        params = {"search": query, "per_page": min(limit, 200), **_mailto()}
        lo, hi = parse_year_range(year)
        filters = []
        if lo is not None:
            filters.append(f"from_publication_date:{lo}-01-01")
        if hi is not None:
            filters.append(f"to_publication_date:{hi}-12-31")
        if filters:
            params["filter"] = ",".join(filters)
        data = get_json(_API, params=params)
        return [_to_paper(w) for w in data.get("results", [])][:limit]

    def fetch(self, paper_id: str) -> Paper | None:
        ident = paper_id.strip()
        doi = normalize_doi(ident)
        if doi:
            url = f"{_API}/doi:{doi}"
        else:
            url = f"{_API}/{ident.rsplit('/', 1)[-1]}"
        data = get_json(url, params=_mailto())
        return _to_paper(data) if data else None
