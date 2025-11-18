import argparse
import json
from datetime import datetime

from app.summarizer.runner import run_daily_summary


def main():
    parser = argparse.ArgumentParser(description="Daily GitHub activity summarizer (CLI)")
    parser.add_argument("--owner", required=True, help="GitHub org/user")
    parser.add_argument("--repo", required=True, help="GitHub repo name")
    parser.add_argument("--date", required=False, help="Day in YYYY-MM-DD (local)")
    parser.add_argument("--golden", required=False, help="Golden summary string for evaluation")
    args = parser.parse_args()

    date = args.date or datetime.utcnow().strftime("%Y-%m-%d")

    state = run_daily_summary(
        owner=args.owner,
        repo=args.repo,
        date=date,
        golden_summary=args.golden,
    )

    print("# Daily summary\n")
    print(state["daily_summary"])
    if state.get("eval_result"):
        print("\n\n# Evaluation\n")
        print(json.dumps(state["eval_result"], indent=2))


if __name__ == "__main__":
    main()
