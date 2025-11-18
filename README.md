# GitHub Daily Activity Summarizer  
*A LangChain + LangGraph pipeline for analyzing GitHub activity, generating daily engineering summaries, and evaluating them with LLMs.*

---

# GitHub Daily Activity Summarizer

## Objective

This project connects to a GitHub repository, collects commits and pull requests for a given day, and generates a concise daily summary:
- Who contributed what  
- What changed in the codebase  
- Which PRs were merged or updated  

It uses **LangChain** and **LangGraph** to structure the data flow, and optionally performs an **LLM-as-a-judge evaluation** against a "golden" reference summary.

---

# Architecture

## High-level flow

1. **Input:**  
   `owner`, `repo`, `date`, optional `golden_summary`

2. **Fetch data from GitHub** (`app/github_client.py`):
   - Commits from `/repos/{owner}/{repo}/commits`
   - Pull Requests from `/repos/{owner}/{repo}/issues`  
   - Date windows adjusted using a configurable **local → UTC** offset (default: UTC+2)

3. **Simplify data** (`app/summarizer/simplify.py`):
   - Extract only needed fields to reduce LLM token usage  
     (author, message, sha, PR title, state, etc.)

4. **Summarization with LangChain** (`app/summarizer/graph_nodes.py`):
   - Commit summary (`commit_summary`)
   - PR summary (`pr_summary`)
   - Final daily summary (`daily_summary`)

5. **LangGraph orchestration** (`app/summarizer/graph_builder.py`):
   The system executes a deterministic pipeline of nodes:
   - `fetch_activity`
   - `summarize_commits`
   - `summarize_prs`
   - `combine_summary`
   - *(optional)* `judge_summary`

6. **Optional evaluation** (`app/summarizer/graph_nodes.py` / `app/evaluation.py`):
   - Compares generated summary with a golden reference  
   - Produces:
     - `coverage` (1–5)  
     - `faithfulness` (1–5)  
     - `clarity` (1–5)  
     - `comments`

---

# Design Decisions & Trade-offs

## Direct API calls vs RAG / Agentic Search

We use **direct GitHub REST API calls**, because:
- GitHub activity data is already structured and filtered
- We only need a single day's activity — no long-term semantic indexing  
- Avoids complexity and cost of RAG/vector databases

We avoid **agentic search**, because:
- Workflow is fully deterministic  
- No tool-calling or dynamic decision-making needed  
- LangGraph’s DAG is a perfect fit

## Why LangChain?

- Modular structured prompts  
- Flexible model selection  
- Clean integration with LangGraph  

## Why LangGraph?

- Explicit graph of nodes  
- Clear state passing  
- Testable, composable workflow  
- Ideal for ETL + summarization pipelines

##  Model Choice: `gpt-4.1-mini`

Selected because:
- Fast  
- Cheap  
- Strong summarization ability  
- Larger models have minimal gains for much higher cost

---

# Running the Project

Below are the **two supported ways** to run this project.

---

# 1. Run via Python CLI

###  Basic usage

python run.py --owner AlaaErfan --repo test-github-activity --date 2025-11-18

# GitHub Activity Summarizer API

A FastAPI-based HTTP API that summarizes GitHub repository activity for a specific date.

# Running the FastAPI Server (HTTP API)

### Start the server


uvicorn app.main:app --reload --port 8000

body of the request
{
  "owner": "AlaaErfan",
  "repo": "test-github-activity",
  "date": "2025-11-18",
  "golden_summary": "On this day, a single contributor made several simple file changes. These included adding a text file, updating its content, renaming it, creating a temporary file, and deleting it. A small test pull request was opened from a feature branch and merged into the main branch. All activity involved basic file edits and PR testing, with no complex code changes."
}




it can be also without the golden_summary

{
  "owner": "AlaaErfan",
  "repo": "test-github-activity",
  "date": "2025-11-18"
}
