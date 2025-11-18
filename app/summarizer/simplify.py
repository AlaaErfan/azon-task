from typing import List, Dict, Any

def simplify_commits(commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    simplified = []
    for c in commits:
        simplified.append({
            "sha": c.get("sha"),
            "author": c.get("commit", {}).get("author", {}).get("name"),
            "message": c.get("commit", {}).get("message"),
            "date": c.get("commit", {}).get("author", {}).get("date"),
        })
    return simplified[:40]


def simplify_prs(prs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    simplified = []
    for p in prs:
        simplified.append({
            "title": p.get("title"),
            "user": p.get("user", {}).get("login"),
            "state": p.get("state"),
            "updated_at": p.get("updated_at"),
        })
    return simplified[:40]
