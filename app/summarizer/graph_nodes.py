import json
from typing import cast

from langchain_openai import ChatOpenAI

from app.config import OPENAI_MODEL, OPENAI_API_KEY
from app.models import RepoState
from app.github_client import day_bounds_local, fetch_commits, fetch_prs
from app.summarizer.prompts import (
    commit_prompt,
    pr_prompt,
    combine_prompt,
    judge_prompt,
)
from app.summarizer.simplify import simplify_commits, simplify_prs

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.2,
    api_key=OPENAI_API_KEY,
)


def fetch_activity(state: RepoState) -> RepoState:
    owner = state["owner"]
    repo = state["repo"]
    date = state["date"]

    since_iso, until_iso = day_bounds_local(date)
    commits = fetch_commits(owner, repo, since_iso, until_iso)
    prs = fetch_prs(owner, repo, since_iso, until_iso)

    new_state = dict(state)
    new_state["commits"] = commits
    new_state["prs"] = prs
    return cast(RepoState, new_state)


def summarize_commits(state: RepoState) -> RepoState:
    commits = state.get("commits", [])
    owner = state["owner"]
    repo = state["repo"]
    date = state["date"]

    simplified = simplify_commits(commits)
    commits_json = json.dumps(simplified, indent=2)

    chain = commit_prompt | llm
    result = chain.invoke(
        {"owner": owner, "repo": repo, "date": date, "commits_json": commits_json}
    )
    summary = getattr(result, "content", str(result))

    new_state = dict(state)
    new_state["commit_summary"] = summary
    return cast(RepoState, new_state)


def summarize_prs(state: RepoState) -> RepoState:
    prs = state.get("prs", [])
    owner = state["owner"]
    repo = state["repo"]
    date = state["date"]

    simplified = simplify_prs(prs)
    prs_json = json.dumps(simplified, indent=2)

    chain = pr_prompt | llm
    result = chain.invoke(
        {"owner": owner, "repo": repo, "date": date, "prs_json": prs_json}
    )
    summary = getattr(result, "content", str(result))

    new_state = dict(state)
    new_state["pr_summary"] = summary
    return cast(RepoState, new_state)


def combine_summary(state: RepoState) -> RepoState:
    owner = state["owner"]
    repo = state["repo"]
    date = state["date"]
    commit_summary = state.get("commit_summary", "No commits.")
    pr_summary = state.get("pr_summary", "No PR activity.")

    chain = combine_prompt | llm
    result = chain.invoke(
        {
            "owner": owner,
            "repo": repo,
            "date": date,
            "commit_summary": commit_summary,
            "pr_summary": pr_summary,
        }
    )
    daily_summary = getattr(result, "content", str(result))

    new_state = dict(state)
    new_state["daily_summary"] = daily_summary
    return cast(RepoState, new_state)


def judge_summary(state: RepoState) -> RepoState:
    golden = state.get("golden_summary")
    if not golden:
        return state

    owner = state["owner"]
    repo = state["repo"]
    date = state["date"]
    generated = state.get("daily_summary", "")

    chain = judge_prompt | llm
    result = chain.invoke(
        {
            "owner": owner,
            "repo": repo,
            "date": date,
            "golden_summary": golden,
            "generated_summary": generated,
        }
    )
    raw = getattr(result, "content", str(result))

    try:
        eval_json = json.loads(raw)
    except json.JSONDecodeError:
        eval_json = {"parse_error": True, "raw": raw}

    new_state = dict(state)
    new_state["eval_result"] = eval_json
    return cast(RepoState, new_state)
