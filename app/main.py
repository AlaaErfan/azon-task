from fastapi import FastAPI
from app.models import SummaryRequest
from app.summarizer.runner import run_daily_summary

app = FastAPI(title="GitHub Activity Summarizer")


@app.post("/summarize")
def summarize(req: SummaryRequest):
    state = run_daily_summary(
        owner=req.owner,
        repo=req.repo,
        date=req.date,
        golden_summary=req.golden_summary,
    )
    return state
