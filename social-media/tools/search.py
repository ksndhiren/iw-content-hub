"""Web search and trend API wrapper."""

from __future__ import annotations

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")


def search(query: str, num_results: int = 5) -> list[dict]:
    """Search the web for trending topics or job market data.

    Returns a list of dicts with keys: title, link, snippet.
    """
    if SERPER_API_KEY:
        return _search_serper(query, num_results)
    elif BRAVE_API_KEY:
        return _search_brave(query, num_results)
    else:
        return _mock_search(query, num_results)


def _search_serper(query: str, num_results: int) -> list[dict]:
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"q": query, "num": num_results}
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    results = resp.json().get("organic", [])
    return [
        {"title": r.get("title", ""), "link": r.get("link", ""), "snippet": r.get("snippet", "")}
        for r in results[:num_results]
    ]


def _search_brave(query: str, num_results: int) -> list[dict]:
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    params = {"q": query, "count": num_results}
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    results = resp.json().get("web", {}).get("results", [])
    return [
        {"title": r.get("title", ""), "link": r.get("url", ""), "snippet": r.get("description", "")}
        for r in results[:num_results]
    ]


def _mock_search(query: str, num_results: int) -> list[dict]:
    """Fallback mock results for dry-run / testing."""
    return [
        {
            "title": f"Mock result for: {query}",
            "link": "https://example.com/mock",
            "snippet": "This is a mock search result. Configure SERPER_API_KEY or BRAVE_API_KEY for real results.",
        }
    ]
