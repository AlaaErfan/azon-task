from typing import Optional
from app.models import RepoState
from app.summarizer.graph_builder import build_graph


def run_daily_summary(
    owner: str,
    repo: str,
    date: str,
    golden_summary: Optional[str] = None,
) -> RepoState:
    include_judge = golden_summary is not None
    app = build_graph(include_judge=include_judge)

    initial_state: RepoState = {
        "owner": owner,
        "repo": repo,
        "date": date,
    }
    if golden_summary:
        initial_state["golden_summary"] = golden_summary

    final_state: RepoState = app.invoke(initial_state)
    return final_state
