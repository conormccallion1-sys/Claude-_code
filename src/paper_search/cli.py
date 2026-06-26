"""Command-line entry point for paper-search."""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .http import session
from .models import Paper, dedup_key, normalize_doi
from .registry import KEYED, PRIORITY_HEALTH, SOURCES, resolve_sources
from .sources.base import SourceError


def _eprint(*args) -> None:
    print(*args, file=sys.stderr)


# ----------------------------------------------------------------------- search
def _search_one(name: str, query: str, limit: int, year: str | None):
    src = SOURCES[name]
    try:
        return name, src.search(query, limit, year), None
    except SourceError as e:
        return name, [], str(e)
    except Exception as e:  # network/parse errors shouldn't kill the whole sweep
        return name, [], f"{type(e).__name__}: {e}"


def _dedup(papers: list[Paper]) -> list[Paper]:
    """Merge duplicates by DOI (or title/author/year), keeping the richest record."""
    merged: dict[str, Paper] = {}
    for p in papers:
        key = dedup_key(p)
        cur = merged.get(key)
        # Keep the record that carries more useful payload (abstract, PDF, DOI...).
        if cur is None or _richness(p) > _richness(cur):
            merged[key] = p
    return list(merged.values())


def _richness(p: Paper) -> int:
    score = 0
    if p.abstract:
        score += 3
    if p.pdf_url:
        score += 2
    if p.doi:
        score += 2
    if p.citations is not None:
        score += 1
    if p.year:
        score += 1
    return score


def cmd_search(args: argparse.Namespace) -> int:
    try:
        names = resolve_sources(args.sources)
    except KeyError as e:
        _eprint(str(e))
        return 2

    results: list[Paper] = []
    errors: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=min(8, len(names))) as ex:
        futs = [ex.submit(_search_one, n, args.query, args.num, args.year) for n in names]
        for fut in as_completed(futs):
            name, papers, err = fut.result()
            if err:
                errors[name] = err
            results.extend(papers)

    deduped = _dedup(results) if not args.no_dedup else results
    payload = {
        "query": args.query,
        "sources": names,
        "year": args.year,
        "total_raw": len(results),
        "total_deduped": len(deduped),
        "errors": errors,
        "results": [p.to_dict() for p in deduped],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    if errors:
        _eprint(f"[{len(errors)} source(s) returned errors; see 'errors' in output]")
    return 0


# --------------------------------------------------------------- download / read
def _resolve_paper(source: str, paper_id: str) -> Paper | None:
    """Find a record (with pdf_url) for source+id, with sensible fallbacks."""
    if source not in SOURCES:
        raise SourceError(f"unknown source: {source}")
    paper = SOURCES[source].fetch(paper_id)
    if paper and paper.pdf_url:
        return paper
    # Fallback chain: resolve an OA PDF by DOI via OpenAlex then Unpaywall.
    doi = normalize_doi(paper_id) or (paper.doi if paper else None)
    if doi:
        for resolver in ("openalex", "unpaywall"):
            try:
                alt = SOURCES[resolver].fetch(doi)
            except SourceError:
                alt = None
            if alt and alt.pdf_url:
                if paper:  # keep the original metadata, borrow the PDF link
                    paper.pdf_url = alt.pdf_url
                    return paper
                return alt
    return paper


def _safe_name(source: str, paper_id: str) -> str:
    base = f"{source}_{paper_id}"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", base)[:120]


def _download_pdf(paper: Paper, out_dir: Path) -> Path:
    if not paper.pdf_url:
        raise SourceError(
            f"no open-access PDF found for {paper.source}:{paper.paper_id}"
            + (f" (doi {paper.doi})" if paper.doi else "")
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{_safe_name(paper.source, paper.paper_id)}.pdf"
    with session().get(paper.pdf_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    fh.write(chunk)
    return dest


def cmd_download(args: argparse.Namespace) -> int:
    try:
        paper = _resolve_paper(args.source, args.paper_id)
        if paper is None:
            _eprint(f"could not resolve {args.source}:{args.paper_id}")
            return 1
        dest = _download_pdf(paper, Path(args.output))
    except SourceError as e:
        _eprint(str(e))
        return 1
    print(json.dumps({
        "source": paper.source,
        "paper_id": paper.paper_id,
        "doi": paper.doi,
        "title": paper.title,
        "pdf_url": paper.pdf_url,
        "path": str(dest),
        "bytes": dest.stat().st_size,
    }, indent=2, ensure_ascii=False))
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    try:
        from pypdf import PdfReader
    except ImportError:
        _eprint("pypdf is required for `read`; install dependencies first")
        return 1
    try:
        paper = _resolve_paper(args.source, args.paper_id)
        if paper is None:
            _eprint(f"could not resolve {args.source}:{args.paper_id}")
            return 1
        dest = _download_pdf(paper, Path(args.output))
    except SourceError as e:
        _eprint(str(e))
        return 1
    try:
        reader = PdfReader(str(dest))
        text = "\n\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as e:
        _eprint(f"failed to extract text: {type(e).__name__}: {e}")
        return 1
    sys.stdout.write(text.strip() + "\n")
    return 0


# --------------------------------------------------------------------- sources
def cmd_sources(args: argparse.Namespace) -> int:
    rows = []
    for name in sorted(SOURCES):
        src = SOURCES[name]
        kind = "search"
        note = ""
        if type(src).__name__ == "_Unavailable":
            kind = "unavailable"
            note = src._reason  # type: ignore[attr-defined]
        elif name == "unpaywall":
            kind = "resolver"
            note = "DOI -> OA PDF (download/read only)"
        if name in KEYED and kind != "unavailable":
            note = (note + "; " if note else "") + f"needs ${KEYED[name]}"
        rows.append({"source": name, "type": kind, "note": note})
    if args.json:
        print(json.dumps({
            "sources": rows,
            "priority_health": PRIORITY_HEALTH,
        }, indent=2, ensure_ascii=False))
        return 0
    width = max(len(r["source"]) for r in rows)
    for r in rows:
        line = f"{r['source']:<{width}}  {r['type']:<12}"
        if r["note"]:
            line += f"  {r['note']}"
        print(line)
    print("\nPriority (health psychology / chronic illness): " + ", ".join(PRIORITY_HEALTH))
    return 0


# ------------------------------------------------------------------------- main
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="paper-search", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("search", help="search across sources (JSON output)")
    s.add_argument("query")
    s.add_argument("-n", "--num", type=int, default=5, help="results per source (default 5)")
    s.add_argument("-s", "--sources", default="all", help='comma list or "all"')
    s.add_argument("-y", "--year", default=None, help='year or range, e.g. 2020 or 2018-2024')
    s.add_argument("--no-dedup", action="store_true", help="skip DOI/title deduplication")
    s.set_defaults(func=cmd_search)

    d = sub.add_parser("download", help="download a PDF by source and id")
    d.add_argument("source")
    d.add_argument("paper_id")
    d.add_argument("-o", "--output", default="./downloads", help="output directory")
    d.set_defaults(func=cmd_download)

    r = sub.add_parser("read", help="download and extract text from a PDF")
    r.add_argument("source")
    r.add_argument("paper_id")
    r.add_argument("-o", "--output", default="./downloads", help="output directory")
    r.set_defaults(func=cmd_read)

    so = sub.add_parser("sources", help="list available sources")
    so.add_argument("--json", action="store_true", help="machine-readable output")
    so.set_defaults(func=cmd_sources)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
