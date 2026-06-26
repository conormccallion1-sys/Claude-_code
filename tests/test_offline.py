"""Offline tests: parsing, dedup and helpers without any network access.

Network egress to academic APIs may be blocked by the session's egress policy,
so these tests mock the HTTP layer and exercise the pure logic.
"""

from __future__ import annotations

import paper_search.http as http
from paper_search.cli import _dedup, _richness
from paper_search.models import Paper, dedup_key, normalize_doi, normalize_title
from paper_search.registry import SOURCES, resolve_sources
from paper_search.sources.base import in_year_range, parse_year_range


# ------------------------------------------------------------------ model helpers
def test_normalize_doi():
    assert normalize_doi("https://doi.org/10.1/AbC") == "10.1/abc"
    assert normalize_doi("doi:10.2/x") == "10.2/x"
    assert normalize_doi(None) is None
    assert normalize_doi("  ") is None


def test_normalize_title():
    assert normalize_title("Hello,  World!") == "hello world"
    assert normalize_title(None) == ""


def test_dedup_key_prefers_doi():
    a = Paper(source="x", paper_id="1", title="T", doi="10.1/A")
    b = Paper(source="y", paper_id="2", title="Different", doi="https://doi.org/10.1/a")
    assert dedup_key(a) == dedup_key(b)


def test_dedup_key_fallback_title():
    a = Paper(source="x", paper_id="1", title="A Study", authors=["Smith J"], year=2020)
    b = Paper(source="y", paper_id="2", title="a study", authors=["smith j"], year=2020)
    assert dedup_key(a) == dedup_key(b)


# -------------------------------------------------------------------- year ranges
def test_parse_year_range():
    assert parse_year_range(None) == (None, None)
    assert parse_year_range("2020") == (2020, 2020)
    assert parse_year_range("2018-2024") == (2018, 2024)
    assert parse_year_range("2018-") == (2018, None)


def test_in_year_range():
    assert in_year_range(2020, "2018-2024")
    assert not in_year_range(2010, "2018-2024")
    assert in_year_range(2010, None)
    assert not in_year_range(None, "2020")


# --------------------------------------------------------------------------- dedup
def test_dedup_keeps_richest():
    poor = Paper(source="a", paper_id="1", title="T", doi="10.1/x")
    rich = Paper(source="b", paper_id="1", title="T", doi="10.1/x",
                 abstract="words", pdf_url="http://p/x.pdf", citations=5, year=2020)
    out = _dedup([poor, rich])
    assert len(out) == 1
    assert out[0].source == "b"
    assert _richness(rich) > _richness(poor)


# ----------------------------------------------------------------- source parsers
def test_openalex_parse(monkeypatch):
    from paper_search.sources import openalex

    fixture = {
        "results": [
            {
                "id": "https://openalex.org/W123",
                "title": "Cortisol and QoL",
                "doi": "https://doi.org/10.1/Q",
                "publication_year": 2021,
                "cited_by_count": 12,
                "authorships": [{"author": {"display_name": "Jane Roe"}}],
                "abstract_inverted_index": {"Hello": [0], "world": [1]},
                "best_oa_location": {"pdf_url": "http://oa/x.pdf"},
                "primary_location": {"source": {"display_name": "J. Endocrinol."}},
            }
        ]
    }
    monkeypatch.setattr(openalex, "get_json", lambda *a, **k: fixture)
    papers = openalex.OpenAlexSource().search("cortisol", 5)
    assert len(papers) == 1
    p = papers[0]
    assert p.title == "Cortisol and QoL"
    assert p.doi == "10.1/q"
    assert p.abstract == "Hello world"
    assert p.pdf_url == "http://oa/x.pdf"
    assert p.authors == ["Jane Roe"]
    assert p.citations == 12


def test_crossref_parse(monkeypatch):
    from paper_search.sources import crossref

    fixture = {
        "message": {
            "items": [
                {
                    "DOI": "10.5/AB",
                    "title": ["A Trial"],
                    "author": [{"given": "Sam", "family": "Lee"}],
                    "issued": {"date-parts": [[2019, 5]]},
                    "container-title": ["BMJ"],
                    "is-referenced-by-count": 3,
                    "link": [{"content-type": "application/pdf", "URL": "http://x/y.pdf"}],
                    "URL": "https://doi.org/10.5/AB",
                }
            ]
        }
    }
    monkeypatch.setattr(crossref, "get_json", lambda *a, **k: fixture)
    papers = crossref.CrossrefSource().search("trial", 5)
    assert papers[0].doi == "10.5/ab"
    assert papers[0].year == 2019
    assert papers[0].authors == ["Sam Lee"]
    assert papers[0].pdf_url == "http://x/y.pdf"


def test_arxiv_parse(monkeypatch):
    from paper_search.sources import arxiv

    xml = """<?xml version='1.0'?>
    <feed xmlns='http://www.w3.org/2005/Atom'>
      <entry>
        <id>http://arxiv.org/abs/2401.01234v2</id>
        <title>Deep Nets</title>
        <summary>An abstract.</summary>
        <published>2024-01-02T00:00:00Z</published>
        <author><name>A. Researcher</name></author>
      </entry>
    </feed>"""
    monkeypatch.setattr(arxiv, "get_text", lambda *a, **k: xml)
    papers = arxiv.ArxivSource().search("deep nets", 5)
    assert papers[0].paper_id == "2401.01234"
    assert papers[0].pdf_url == "https://arxiv.org/pdf/2401.01234.pdf"
    assert papers[0].year == 2024
    assert papers[0].authors == ["A. Researcher"]


def test_europepmc_parse(monkeypatch):
    from paper_search.sources import europepmc

    fixture = {
        "resultList": {
            "result": [
                {
                    "doi": "10.9/ZZ",
                    "title": "Preprint",
                    "authorString": "Doe J, Roe K.",
                    "pubYear": "2022",
                    "abstractText": "Body.",
                    "journalTitle": "bioRxiv",
                    "citedByCount": 1,
                    "pmcid": "PMC999",
                    "source": "PMC",
                }
            ]
        }
    }
    monkeypatch.setattr(europepmc, "get_json", lambda *a, **k: fixture)
    papers = europepmc.BioRxivSource().search("x", 5)
    assert papers[0].source == "biorxiv"
    assert papers[0].doi == "10.9/zz"
    assert papers[0].authors == ["Doe J", "Roe K"]
    assert papers[0].year == 2022
    assert "fullTextPDF" in papers[0].pdf_url


# ------------------------------------------------------------------------ registry
def test_resolve_sources_all():
    names = resolve_sources("all")
    assert "openalex" in names and "pubmed" in names


def test_resolve_sources_unknown():
    try:
        resolve_sources("not_a_real_source")
    except KeyError as e:
        assert "unknown" in str(e)
    else:
        raise AssertionError("expected KeyError")


def test_unavailable_source_raises():
    from paper_search.sources.base import SourceUnavailable

    try:
        SOURCES["google_scholar"].search("x", 1)
    except SourceUnavailable:
        pass
    else:
        raise AssertionError("expected SourceUnavailable")
