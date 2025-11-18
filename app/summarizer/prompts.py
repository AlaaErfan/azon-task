from langchain_core.prompts import ChatPromptTemplate

commit_prompt = ChatPromptTemplate.from_template(
    """You are a senior engineering lead summarizing daily Git commit activity.

Repository: {owner}/{repo}
Date (local): {date}

Here is simplified JSON for all commits that happened in that day:

{commits_json}

Tasks:
1. Group work by contributor.
2. Summarize what each contributor worked on, focusing on behavior changes and refactors.
3. Mention notable files or domains (e.g., auth, infra) instead of line-level details.
4. Be concise but informative.

Output in Markdown with headings:
- "Commits overview"
- "Work by contributor"
"""
)

pr_prompt = ChatPromptTemplate.from_template(
    """You are a senior engineering lead summarizing daily PR activity.

Repository: {owner}/{repo}
Date (local): {date}

Here is simplified JSON for all pull requests that were updated that day:

{prs_json}

Tasks:
1. Summarize PRs merged, including what they change and why they matter.
2. List PRs still open but updated that day.
3. Highlight any risky or breaking changes if visible from titles/descriptions.

Output in Markdown with headings:
- "PRs merged"
- "Open PRs updated"
"""
)

combine_prompt = ChatPromptTemplate.from_template(
    """You are generating a daily engineering activity report.

Repository: {owner}/{repo}
Date (local): {date}

Commit summary:
---
{commit_summary}
---

PR summary:
---
{pr_summary}
---

Now produce a final daily report.

Requirements:
- Start with a short executive summary (3–5 bullet points).
- Then have sections:
  - "Who contributed what"
  - "Code changes overview"
  - "Pull requests"
- In "Who contributed what", list each contributor with 1–3 bullets describing their main work.
- Keep it concise but high-signal, suitable for a team Slack update.

Output in Markdown.
"""
)

judge_prompt = ChatPromptTemplate.from_template(
    """You are an LLM judge evaluating a generated daily GitHub activity summary.

Repository: {owner}/{repo}
Date (local): {date}

GOLDEN REFERENCE SUMMARY:
---
{golden_summary}
---

GENERATED SUMMARY:
---
{generated_summary}
---

Evaluate on:
1. Coverage: Does it cover the main contributors and changes?
2. Faithfulness: Does it avoid hallucinations compared to the golden?
3. Clarity: Is it easy to read and structured?

Return a JSON object with keys:
- "coverage": integer from 1 to 5
- "faithfulness": integer from 1 to 5
- "clarity": integer from 1 to 5
- "comments": short free-text comment

Return ONLY valid JSON, no extra text.
"""
)
