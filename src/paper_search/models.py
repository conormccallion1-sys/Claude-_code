"""Shared data model for a paper record and small normalisation helpers."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field


@dataclass
class Paper:
    """A single normalised paper record returned by any source."""

    source: str
    paper_id: str
    title: str
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    doi: str | None = None
    abstract: str | None = None
    url: str | None = None
    pdf_url: str | None = None
    venue: str | None = None
    citations: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_doi(doi: str | None) -> str | None:
    """Lowercase a DOI and strip any URL/`doi:` prefix for stable dedup keys."""
    if not doi:
        return None
    doi = doi.strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi or None


def normalize_title(title: str | None) -> str:
    """Collapse whitespace and punctuation so titles compare reliably."""
    if not title:
        return ""
    title = title.lower()
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return title.strip()


def dedup_key(paper: Paper) -> str:
    """Prefer DOI; otherwise fall back to title + first author + year."""
    doi = normalize_doi(paper.doi)
    if doi:
        return f"doi:{doi}"
    first_author = (paper.authors[0].lower().strip() if paper.authors else "")
    return f"t:{normalize_title(paper.title)}|a:{first_author}|y:{paper.year or ''}"
