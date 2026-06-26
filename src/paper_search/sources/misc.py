"""Additional sources with simple public JSON APIs.

Grouped here to keep the per-source boilerplate compact: DOAJ, DBLP, Zenodo,
HAL, OpenAIRE and CORE.
"""

from __future__ import annotations

import os

from ..http import get_json
from ..models import Paper, normalize_doi
from .base import Source, SourceError, in_year_range, parse_year_range


# --------------------------------------------------------------------------- DOAJ
class DOAJSource(Source):
    name = "doaj"
    _API = "https://doaj.org/api/v2/search/articles"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        data = get_json(f"{self._API}/{query}", params={"pageSize": min(limit, 100)})
        out = []
        for r in data.get("results", []):
            b = r.get("bibjson") or {}
            doi = None
            pdf_url = None
            url = None
            for ident in b.get("identifier") or []:
                if ident.get("type") == "doi":
                    doi = normalize_doi(ident.get("id"))
            for link in b.get("link") or []:
                if link.get("type") == "fulltext":
                    url = link.get("url")
                    if (link.get("content_type") or "").lower() == "application/pdf":
                        pdf_url = link.get("url")
            year_val = int(b["year"]) if str(b.get("year", "")).isdigit() else None
            if not in_year_range(year_val, year):
                continue
            out.append(
                Paper(
                    source=self.name,
                    paper_id=doi or r.get("id") or "",
                    title=b.get("title") or "",
                    authors=[a.get("name", "") for a in b.get("author") or []],
                    year=year_val,
                    doi=doi,
                    abstract=b.get("abstract"),
                    url=url,
                    pdf_url=pdf_url,
                    venue=(b.get("journal") or {}).get("title"),
                )
            )
            if len(out) >= limit:
                break
        return out


# --------------------------------------------------------------------------- DBLP
class DBLPSource(Source):
    name = "dblp"
    _API = "https://dblp.org/search/publ/api"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        data = get_json(
            self._API, params={"q": query, "format": "json", "h": min(limit * 2, 100)}
        )
        hits = ((data.get("result") or {}).get("hits") or {}).get("hit") or []
        out = []
        for h in hits:
            info = h.get("info") or {}
            year_val = int(info["year"]) if str(info.get("year", "")).isdigit() else None
            if not in_year_range(year_val, year):
                continue
            authors_field = (info.get("authors") or {}).get("author") or []
            if isinstance(authors_field, dict):
                authors_field = [authors_field]
            authors = [a.get("text", "") if isinstance(a, dict) else str(a) for a in authors_field]
            out.append(
                Paper(
                    source=self.name,
                    paper_id=normalize_doi(info.get("doi")) or info.get("key") or "",
                    title=info.get("title") or "",
                    authors=authors,
                    year=year_val,
                    doi=normalize_doi(info.get("doi")),
                    url=info.get("ee") or info.get("url"),
                    venue=info.get("venue"),
                )
            )
            if len(out) >= limit:
                break
        return out


# ------------------------------------------------------------------------- Zenodo
class ZenodoSource(Source):
    name = "zenodo"
    _API = "https://zenodo.org/api/records"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        params = {"q": query, "size": min(limit, 100), "sort": "bestmatch"}
        if os.environ.get("ZENODO_TOKEN"):
            params["access_token"] = os.environ["ZENODO_TOKEN"]
        data = get_json(self._API, params=params)
        out = []
        for r in data.get("hits", {}).get("hits", []):
            md = r.get("metadata") or {}
            pub = md.get("publication_date") or ""
            year_val = int(pub[:4]) if pub[:4].isdigit() else None
            if not in_year_range(year_val, year):
                continue
            pdf_url = None
            for f in r.get("files") or []:
                if (f.get("key") or "").lower().endswith(".pdf"):
                    pdf_url = (f.get("links") or {}).get("self")
                    break
            out.append(
                Paper(
                    source=self.name,
                    paper_id=normalize_doi(md.get("doi")) or str(r.get("id") or ""),
                    title=md.get("title") or "",
                    authors=[c.get("name", "") for c in md.get("creators") or []],
                    year=year_val,
                    doi=normalize_doi(md.get("doi")),
                    abstract=md.get("description"),
                    url=(r.get("links") or {}).get("html"),
                    pdf_url=pdf_url,
                    venue="Zenodo",
                )
            )
            if len(out) >= limit:
                break
        return out


# ---------------------------------------------------------------------------- HAL
class HALSource(Source):
    name = "hal"
    _API = "https://api.archives-ouvertes.fr/search/"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        params = {
            "q": query,
            "rows": min(limit, 100),
            "fl": "docid,title_s,authFullName_s,producedDateY_i,doiId_s,abstract_s,uri_s,fileMain_s,journalTitle_s",
            "wt": "json",
        }
        lo, hi = parse_year_range(year)
        if lo is not None or hi is not None:
            params["fq"] = f"producedDateY_i:[{lo or 1900} TO {hi or 2100}]"
        data = get_json(self._API, params=params)
        out = []
        for d in (data.get("response") or {}).get("docs", []):
            title = d.get("title_s") or []
            out.append(
                Paper(
                    source=self.name,
                    paper_id=normalize_doi(d.get("doiId_s")) or str(d.get("docid") or ""),
                    title=title[0] if isinstance(title, list) and title else (title or ""),
                    authors=d.get("authFullName_s") or [],
                    year=d.get("producedDateY_i"),
                    doi=normalize_doi(d.get("doiId_s")),
                    abstract=(d.get("abstract_s") or [None])[0] if isinstance(d.get("abstract_s"), list) else d.get("abstract_s"),
                    url=d.get("uri_s"),
                    pdf_url=d.get("fileMain_s"),
                    venue=d.get("journalTitle_s"),
                )
            )
        return out[:limit]


# ------------------------------------------------------------------------ OpenAIRE
class OpenAIRESource(Source):
    name = "openaire"
    _API = "https://api.openaire.eu/search/publications"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        # OpenAIRE returns JSON when format=json is requested.
        params = {"keywords": query, "size": min(limit, 50), "format": "json"}
        lo, hi = parse_year_range(year)
        if lo is not None:
            params["fromDateAccepted"] = f"{lo}-01-01"
        if hi is not None:
            params["toDateAccepted"] = f"{hi}-12-31"
        data = get_json(self._API, params=params)
        results = (((data.get("response") or {}).get("results") or {}) or {}).get("result") or []
        out = []
        for r in results:
            meta = (((r.get("metadata") or {}).get("oaf:entity") or {}).get("oaf:result") or {})
            title = meta.get("title")
            if isinstance(title, list):
                title = title[0]
            if isinstance(title, dict):
                title = title.get("$") or title.get("content") or ""
            doi = None
            for pid in _as_list(meta.get("pid")):
                if isinstance(pid, dict) and pid.get("@classid") == "doi":
                    doi = normalize_doi(pid.get("$"))
            date = meta.get("dateofacceptance")
            if isinstance(date, dict):
                date = date.get("$")
            year_val = int(str(date)[:4]) if date and str(date)[:4].isdigit() else None
            if not in_year_range(year_val, year):
                continue
            out.append(
                Paper(
                    source=self.name,
                    paper_id=doi or "",
                    title=title or "",
                    authors=[c.get("$", "") for c in _as_list(meta.get("creator")) if isinstance(c, dict)],
                    year=year_val,
                    doi=doi,
                    url=f"https://doi.org/{doi}" if doi else None,
                    venue="OpenAIRE",
                )
            )
            if len(out) >= limit:
                break
        return out


def _as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


# --------------------------------------------------------------------------- CORE
class CORESource(Source):
    name = "core"
    requires = ("CORE_API_KEY",)
    _API = "https://api.core.ac.uk/v3/search/works"

    def search(self, query: str, limit: int, year: str | None = None) -> list[Paper]:
        key = os.environ.get("CORE_API_KEY")
        if not key:
            raise SourceError("core requires the CORE_API_KEY environment variable")
        q = query
        lo, hi = parse_year_range(year)
        if lo is not None:
            q += f" AND yearPublished>={lo}"
        if hi is not None:
            q += f" AND yearPublished<={hi}"
        data = get_json(
            self._API,
            params={"q": q, "limit": min(limit, 100)},
            headers={"Authorization": f"Bearer {key}"},
        )
        out = []
        for r in data.get("results", []):
            doi = normalize_doi(r.get("doi"))
            out.append(
                Paper(
                    source=self.name,
                    paper_id=doi or str(r.get("id") or ""),
                    title=r.get("title") or "",
                    authors=[a.get("name", "") for a in r.get("authors") or []],
                    year=r.get("yearPublished"),
                    doi=doi,
                    abstract=r.get("abstract"),
                    url=r.get("sourceFulltextUrls", [None])[0] if r.get("sourceFulltextUrls") else None,
                    pdf_url=r.get("downloadUrl"),
                    venue=r.get("publisher"),
                )
            )
        return out[:limit]
