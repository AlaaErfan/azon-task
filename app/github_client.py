import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Tuple

from app.config import GITHUB_TOKEN, TZ_OFFSET_HOURS

GITHUB_API_BASE = "https://api.github.com"


def github_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def day_bounds_local(date_str: str) -> Tuple[str, str]:
    """
    Given a local date 'YYYY-MM-DD', return (since_iso, until_iso)
    as UTC ISO timestamps that span that local day.
    """
    offset = timezone(timedelta(hours=TZ_OFFSET_HOURS))
    day_local = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=offset)
    next_day_local = day_local + timedelta(days=1)

    day_utc = day_local.astimezone(timezone.utc)
    next_day_utc = next_day_local.astimezone(timezone.utc)

    return day_utc.isoformat(), next_day_utc.isoformat()


def fetch_commits(owner: str, repo: str, since_iso: str, until_iso: str) -> List[Dict[str, Any]]:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
    params = {"since": since_iso, "until": until_iso, "per_page": 100}
    commits: List[Dict[str, Any]] = []

    while True:
        resp = requests.get(url, headers=github_headers(), params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        commits.extend(batch)

        links = resp.headers.get("Link", "")
        next_url = None
        if links:
            for part in links.split(","):
                if 'rel="next"' in part:
                    next_url = part.split(";")[0].strip(" <>")
        if not next_url:
            break
        url = next_url
        params = {}

    return commits


def fetch_prs(owner: str, repo: str, since_iso: str, until_iso: str) -> List[Dict[str, Any]]:
    """
    Use issues API (which includes PRs) and filter by updated_at window.
    """
    search_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    params = {"since": since_iso, "state": "all", "per_page": 100}
    prs: List[Dict[str, Any]] = []

    while True:
        resp = requests.get(search_url, headers=github_headers(), params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break

        for item in batch:
            if "pull_request" in item:
                updated_at = item.get("updated_at")
                if updated_at and since_iso <= updated_at <= until_iso:
                    prs.append(item)

        links = resp.headers.get("Link", "")
        next_url = None
        if links:
            for part in links.split(","):
                if 'rel="next"' in part:
                    next_url = part.split(";")[0].strip(" <>")
        if not next_url:
            break
        search_url = next_url
        params = {}

    return prs
