"""Europe PMC REST API.

Europe PMC indexes PubMed, PMC, Agricola, preprint servers and more, so it
also backs the `pmc`, `biorxiv` and `medrxiv` sources via source/publisher
filters. Each is exposed as its own Source subclass with a fixed filter.
"""

from __future__ import annotations

from ..http import get_json
from ..models import Paper, normalize_doi
from .base import Source, parse_year_range

_API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def _to_paper(r: dict, source_name: str) -> Paper:
    doi = normalize_doi(r.get("doi"))
    pmcid = r.get("pmcid")
    pdf_url = None
    if pmcid:
        pdf_url = (
            f"https://www.ebi.ac.uk/europepmc/webservices/rest/{r.get('source','PMC')}/"
            f"{pmcid}/fullTextPDF"
        )
    year = None
    if r.get("pubYear") and str(r["pubYear"]).isdigit():
        year = int(r["pubYear"])
    authors = []
    if r.get("authorString"):
        authors = [a.strip() for a in r["authorString"].rstrip(".").split(",") if a.strip()]
    return Paper(
        source=source_name,
        paper_id=doi or pmcid or r.get("id") or "",
        title=r.get("title") or "",
        authors=authors,
        year=year,
        doi=doi,
        abstract=r.get("abstractText"),
        url=(f"https://doi.org/{doi}" if doi else r.get("fullTextUrlList", {}).get("url")),
        pdf_url=pdf_url,
        venue=r.get("journalTitle"),
        citations=r.get("citedByCount"),
    )


class _EuropePMCBase(Source):
    # Extra Europe PMC query fragment appended with AND (empty for the base source).
    extra_query: str = ""

    def _query(self, query: str, year: str | None) -> str:
        parts = [f"({query})"]
        if self.extra_query:
            parts.append(self.extra_query)
        lo, hi = parse_year_range(year)
        if lo is not None or hi is not None:
            lo = lo or 1900
            hi = hi or 2100
            parts.append(f"(PUB_YEAR:[{lo} TO {hi}])")
        return " AND ".join(parts)

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        data = get_json(
            _API,
            params={
                "query": self._query(query, year),
                "format": "json",
                "pageSize": min(limit, 100),
                "resultType": "core",
            },
        )
        results = (data.get("resultList") or {}).get("result") or []
        return [_to_paper(r, self.name) for r in results][:limit]

    def fetch(self, paper_id: str) -> Paper | None:
        doi = normalize_doi(paper_id)
        q = f"DOI:{doi}" if doi else paper_id
        data = get_json(
            _API, params={"query": q, "format": "json", "pageSize": 1, "resultType": "core"}
        )
        results = (data.get("resultList") or {}).get("result") or []
        return _to_paper(results[0], self.name) if results else None


class EuropePMCSource(_EuropePMCBase):
    name = "europepmc"
    extra_query = ""


class PMCSource(_EuropePMCBase):
    name = "pmc"
    extra_query = "(IN_EPMC:Y AND OPEN_ACCESS:Y)"


class BioRxivSource(_EuropePMCBase):
    name = "biorxiv"
    extra_query = '(SRC:PPR AND PUBLISHER:"bioRxiv")'


class MedRxivSource(_EuropePMCBase):
    name = "medrxiv"
    extra_query = '(SRC:PPR AND PUBLISHER:"medRxiv")'
