ALLOWED_LABELS = {"time_sensitive", "not_time_sensitive"}


def run_checks(rows):
    """Return a list of (id, issue) tuples for rule violations."""
    issues = []
    seen_ids = set()

    for row in rows:
        row_id = row["id"]

        if row_id in seen_ids:
            issues.append((row_id, "duplicate id"))
        seen_ids.add(row_id)

        if row["label"] not in ALLOWED_LABELS:
            issues.append((row_id, f"invalid label: {row['label']}"))

        if not row["text"].strip():
            issues.append((row_id, "empty text"))

    return issues