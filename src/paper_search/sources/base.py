"""Base class and shared helpers for all sources."""

from __future__ import annotations

from ..models import Paper


class SourceError(RuntimeError):
    """Raised when a source cannot fulfil a request (network, no key, etc.)."""


class SourceUnavailable(SourceError):
    """Raised when a source has no usable public API in this CLI."""


class Source:
    """Interface every source implements.

    `name` is the short identifier used on the command line.
    `requires` lists environment variables needed (empty for keyless sources).
    """

    name: str = ""
    requires: tuple[str, ...] = ()

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        raise NotImplementedError

    def fetch(self, paper_id: str) -> Paper | None:
        """Resolve a single record (with a pdf_url where possible) by id/DOI.

        Default implementation returns None; sources override when they can.
        The CLI falls back to OpenAlex/Unpaywall DOI resolution when this is None.
        """
        return None


def parse_year_range(year: str | None) -> tuple[int | None, int | None]:
    """Parse `-y` values: "2020" -> (2020, 2020); "2018-2024" -> (2018, 2024)."""
    if not year:
        return (None, None)
    year = year.strip()
    if "-" in year:
        lo, _, hi = year.partition("-")
        return (int(lo) if lo else None, int(hi) if hi else None)
    y = int(year)
    return (y, y)


def in_year_range(value: int | None, year: str | None) -> bool:
    """Client-side year filter for sources that cannot filter server-side."""
    lo, hi = parse_year_range(year)
    if lo is None and hi is None:
        return True
    if value is None:
        return False
    if lo is not None and value < lo:
        return False
    if hi is not None and value > hi:
        return False
    return True
