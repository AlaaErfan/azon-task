from typing import Dict, Any
from app.summarizer.runner import run_daily_summary


def evaluate_with_golden(
    owner: str,
    repo: str,
    date: str,
    golden_summary: str,
) -> Dict[str, Any]:
    state = run_daily_summary(owner, repo, date, golden_summary=golden_summary)
    return {
        "daily_summary": state.get("daily_summary"),
        "eval_result": state.get("eval_result"),
    }
