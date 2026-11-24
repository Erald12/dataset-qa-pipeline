import csv
import time
from pathlib import Path

from src.checks import run_checks
from src.review import review_row

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "incoming" / "data.csv"
OUTPUT = ROOT / "output" / "report.csv"


def main():
    start = time.time()

    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Group rule-based issues by row ID
    issue_map = {}
    for row_id, issue in run_checks(rows):
        issue_map.setdefault(row_id, []).append(issue)

    OUTPUT.parent.mkdir(exist_ok=True)
    flagged = 0

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "python_issues", "claude_correct", "claude_reason"])

        for row in rows:
            if row["text"].strip():
                result = review_row(row)
            else:
                # Nothing for Claude to judge in an empty row
                result = {"correct": None, "reason": "skipped: empty text"}

            py_issues = "; ".join(issue_map.get(row["id"], []))
            if py_issues or result["correct"] is False:
                flagged += 1

            writer.writerow([row["id"], py_issues, result["correct"], result["reason"]])

    elapsed = time.time() - start
    print(f"Reviewed {len(rows)} rows, flagged {flagged}, in {elapsed:.1f}s")
    print(f"Report written to {OUTPUT}")


if __name__ == "__main__":
    main()