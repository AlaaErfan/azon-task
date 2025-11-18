from langgraph.graph import StateGraph, END
from app.models import RepoState
from app.summarizer.graph_nodes import (
    fetch_activity,
    summarize_commits,
    summarize_prs,
    combine_summary,
    judge_summary,
)


def build_graph(include_judge: bool = True):
    graph = StateGraph(RepoState)

    graph.add_node("fetch_activity", fetch_activity)
    graph.add_node("summarize_commits", summarize_commits)
    graph.add_node("summarize_prs", summarize_prs)
    graph.add_node("combine_summary", combine_summary)

    if include_judge:
        graph.add_node("judge_summary", judge_summary)

    graph.add_edge("__start__", "fetch_activity")
    graph.add_edge("fetch_activity", "summarize_commits")
    graph.add_edge("summarize_commits", "summarize_prs")
    graph.add_edge("summarize_prs", "combine_summary")

    if include_judge:
        graph.add_edge("combine_summary", "judge_summary")
        graph.add_edge("judge_summary", END)
    else:
        graph.add_edge("combine_summary", END)

    return graph.compile()
