"""A shared requests session with sensible retries and a descriptive UA."""

from __future__ import annotations

import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_CONTACT = os.environ.get("PAPER_SEARCH_EMAIL", "paper-search@example.com")
USER_AGENT = f"paper-search/0.1 (mailto:{_CONTACT})"

_session: requests.Session | None = None


def session() -> requests.Session:
    """Return a process-wide session with retry/backoff configured once."""
    global _session
    if _session is None:
        s = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "POST"),
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        s.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
        _session = s
    return _session


def get_json(url: str, params: dict | None = None, timeout: int = 30, **kw) -> dict:
    r = session().get(url, params=params, timeout=timeout, **kw)
    r.raise_for_status()
    return r.json()


def get_text(url: str, params: dict | None = None, timeout: int = 30, **kw) -> str:
    r = session().get(url, params=params, timeout=timeout, **kw)
    r.raise_for_status()
    return r.text
