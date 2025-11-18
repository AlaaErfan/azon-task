from typing import List, Dict, Any, Optional, TypedDict
from pydantic import BaseModel

class RepoState(TypedDict, total=False):
    owner: str
    repo: str
    date: str  # YYYY-MM-DD (local day)
    commits: List[Dict[str, Any]]
    prs: List[Dict[str, Any]]
    commit_summary: str
    pr_summary: str
    daily_summary: str
    golden_summary: Optional[str]
    eval_result: Optional[Dict[str, Any]]

class SummaryRequest(BaseModel):
    owner: str
    repo: str
    date: str
    golden_summary: Optional[str] = None
