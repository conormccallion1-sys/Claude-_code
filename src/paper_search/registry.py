"""Source registry: names -> Source instances, plus metadata for the CLI."""

from __future__ import annotations

from .sources.arxiv import ArxivSource
from .sources.base import Source, SourceUnavailable
from .sources.crossref import CrossrefSource
from .sources.europepmc import (
    BioRxivSource,
    EuropePMCSource,
    MedRxivSource,
    PMCSource,
)
from .sources.misc import (
    CORESource,
    DBLPSource,
    DOAJSource,
    HALSource,
    OpenAIRESource,
    ZenodoSource,
)
from .sources.openalex import OpenAlexSource
from .sources.pubmed import PubMedSource
from .sources.semantic import SemanticScholarSource
from .sources.unpaywall import UnpaywallSource


class _Unavailable(Source):
    """Placeholder for sources with no usable public keyword API in this CLI."""

    def __init__(self, name: str, reason: str):
        self.name = name
        self._reason = reason

    def search(self, query, limit, year=None):
        raise SourceUnavailable(f"{self.name}: {self._reason}")


# Sources with no public keyword API we can call without scraping/credentials.
_UNAVAILABLE = {
    "google_scholar": "no public API (scraping is blocked); use semantic/openalex instead",
    "iacr": "no JSON search API; browse https://eprint.iacr.org directly",
    "citeseerx": "no stable public search API",
    "base": "requires an allow-listed IP / OAI registration",
    "ssrn": "no public search API",
    "ieee": "requires IEEE_API_KEY and a subscription",
    "acm": "requires ACM_API_KEY and a subscription",
}


def _build() -> dict[str, Source]:
    impls: list[Source] = [
        ArxivSource(),
        PubMedSource(),
        PMCSource(),
        EuropePMCSource(),
        BioRxivSource(),
        MedRxivSource(),
        SemanticScholarSource(),
        CrossrefSource(),
        OpenAlexSource(),
        DOAJSource(),
        DBLPSource(),
        OpenAIRESource(),
        ZenodoSource(),
        HALSource(),
        CORESource(),
        UnpaywallSource(),
    ]
    registry: dict[str, Source] = {s.name: s for s in impls}
    for name, reason in _UNAVAILABLE.items():
        registry[name] = _Unavailable(name, reason)
    return registry


SOURCES: dict[str, Source] = _build()

# Sources used for a default "all" sweep (keyword-searchable, keyless, reliable).
DEFAULT_SOURCES = [
    "arxiv", "pubmed", "pmc", "europepmc", "biorxiv", "medrxiv",
    "semantic", "crossref", "openalex", "doaj", "dblp", "openaire",
    "zenodo", "hal",
]

# Recommended ordering for health-psychology / chronic-illness work.
PRIORITY_HEALTH = [
    "pubmed", "pmc", "europepmc", "semantic", "crossref", "openalex", "medrxiv", "doaj",
]

# Sources that need credentials/email before they will return results.
KEYED = {
    "core": "CORE_API_KEY",
    "unpaywall": "PAPER_SEARCH_EMAIL",
    "ieee": "IEEE_API_KEY",
    "acm": "ACM_API_KEY",
}


def resolve_sources(spec: str | None) -> list[str]:
    """Turn a `-s` spec ("all", or comma list) into concrete source names."""
    if not spec or spec.strip().lower() == "all":
        return list(DEFAULT_SOURCES)
    names = [s.strip() for s in spec.split(",") if s.strip()]
    unknown = [n for n in names if n not in SOURCES]
    if unknown:
        raise KeyError(f"unknown source(s): {', '.join(unknown)}")
    return names
