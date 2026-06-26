"""arXiv via the public Atom export API."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

from ..http import get_text
from ..models import Paper
from .base import Source, in_year_range

_NS = {"a": "http://www.w3.org/2005/Atom"}
_API = "http://export.arxiv.org/api/query"


def _clean(text: str | None) -> str | None:
    if text is None:
        return None
    return re.sub(r"\s+", " ", text).strip() or None


def _arxiv_id(entry: ET.Element) -> str:
    raw = entry.findtext("a:id", default="", namespaces=_NS)
    # https://arxiv.org/abs/2401.01234v2 -> 2401.01234
    m = re.search(r"abs/([^v]+)", raw)
    return (m.group(1) if m else raw).strip()


class ArxivSource(Source):
    name = "arxiv"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        text = get_text(
            _API,
            params={
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": max(limit * 2, limit),  # over-fetch for year filtering
                "sortBy": "relevance",
            },
        )
        root = ET.fromstring(text)
        papers: list[Paper] = []
        for entry in root.findall("a:entry", _NS):
            published = entry.findtext("a:published", default="", namespaces=_NS)
            year_val = int(published[:4]) if published[:4].isdigit() else None
            if not in_year_range(year_val, year):
                continue
            pid = _arxiv_id(entry)
            doi = _clean(entry.findtext("a:doi", namespaces=_NS))
            papers.append(
                Paper(
                    source=self.name,
                    paper_id=pid,
                    title=_clean(entry.findtext("a:title", namespaces=_NS)) or "",
                    authors=[
                        _clean(a.findtext("a:name", namespaces=_NS)) or ""
                        for a in entry.findall("a:author", _NS)
                    ],
                    year=year_val,
                    doi=doi,
                    abstract=_clean(entry.findtext("a:summary", namespaces=_NS)),
                    url=f"https://arxiv.org/abs/{pid}",
                    pdf_url=f"https://arxiv.org/pdf/{pid}.pdf",
                    venue="arXiv",
                )
            )
            if len(papers) >= limit:
                break
        return papers

    def fetch(self, paper_id: str) -> Paper | None:
        pid = re.sub(r"^arxiv:", "", paper_id, flags=re.I).strip()
        # arXiv's id_list param is the reliable single-record lookup.
        text = get_text(_API, params={"id_list": pid, "max_results": 1})
        root = ET.fromstring(text)
        entry = root.find("a:entry", _NS)
        if entry is None:
            return None
        published = entry.findtext("a:published", default="", namespaces=_NS)
        year_val = int(published[:4]) if published[:4].isdigit() else None
        rid = _arxiv_id(entry)
        return Paper(
            source=self.name,
            paper_id=rid,
            title=_clean(entry.findtext("a:title", namespaces=_NS)) or "",
            authors=[
                _clean(a.findtext("a:name", namespaces=_NS)) or ""
                for a in entry.findall("a:author", _NS)
            ],
            year=year_val,
            doi=_clean(entry.findtext("a:doi", namespaces=_NS)),
            abstract=_clean(entry.findtext("a:summary", namespaces=_NS)),
            url=f"https://arxiv.org/abs/{rid}",
            pdf_url=f"https://arxiv.org/pdf/{rid}.pdf",
            venue="arXiv",
        )
