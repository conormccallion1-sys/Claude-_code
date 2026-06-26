"""Unpaywall: a DOI -> open-access PDF resolver (no keyword search)."""

from __future__ import annotations

import os

from ..http import get_json
from ..models import Paper, normalize_doi
from .base import Source, SourceError


class UnpaywallSource(Source):
    """Resolver-only source. `search` is unsupported; `fetch` resolves a DOI."""

    name = "unpaywall"
    requires = ("PAPER_SEARCH_EMAIL",)
    _API = "https://api.unpaywall.org/v2"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        raise SourceError(
            "unpaywall has no keyword search; use it via `download`/`read` to resolve a DOI"
        )

    def fetch(self, paper_id: str) -> Paper | None:
        doi = normalize_doi(paper_id)
        if not doi:
            return None
        email = os.environ.get("PAPER_SEARCH_EMAIL")
        if not email:
            raise SourceError("unpaywall requires the PAPER_SEARCH_EMAIL environment variable")
        data = get_json(f"{self._API}/{doi}", params={"email": email})
        if not data:
            return None
        loc = data.get("best_oa_location") or {}
        return Paper(
            source=self.name,
            paper_id=doi,
            title=data.get("title") or "",
            authors=[
                " ".join(p for p in (a.get("given"), a.get("family")) if p)
                for a in (data.get("z_authors") or [])
            ],
            year=data.get("year"),
            doi=doi,
            url=data.get("doi_url"),
            pdf_url=loc.get("url_for_pdf") or loc.get("url"),
            venue=data.get("journal_name"),
        )
