"""Summarize human-reviewed GEO observations without contacting engines."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def summarize(document):
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("Expected an object with schema_version 1")
    if not isinstance(document.get("runs"), list):
        raise ValueError("runs must be an array")
    groups = defaultdict(Counter)
    keys = set()
    for run in document["runs"]:
        if not isinstance(run, dict):
            raise ValueError("Each run must be an object")
        fields = ("window", "surface", "locale", "intent", "query_id", "run_id")
        if any(not isinstance(run.get(field), str) or not run[field].strip() for field in fields):
            raise ValueError("Every run requires non-empty window, surface, locale, intent, query_id and run_id")
        identity = tuple(run[field] for field in fields)
        if identity in keys:
            raise ValueError("Duplicate run")
        keys.add(identity)
        counts = groups[identity[:4]]
        state = run.get("state")
        if state not in ("observed", "failed", "not_run"):
            raise ValueError("Invalid run state")
        counts[state] += 1
        if state == "observed":
            for field in ("mentioned", "cited"):
                value = run.get(field)
                if value is not None and type(value) is not bool:
                    raise ValueError(f"{field} must be boolean or null")
                if value is None:
                    counts[field + "_unknown"] += 1
                elif value:
                    counts[field] += 1
        elif any(run.get(field) is not None for field in ("mentioned", "cited")):
            raise ValueError("Only observed runs may have scores")

    rows = []
    for (window, surface, locale, intent), counts in sorted(groups.items()):
        row = {"window":window, "surface":surface, "locale":locale, "intent":intent}
        row.update({key:counts[key] for key in ("observed", "failed", "not_run")})
        for field in ("mentioned", "cited"):
            denominator = counts["observed"] - counts[field + "_unknown"]
            row[field] = {"yes":counts[field], "scored":denominator, "unknown":counts[field + "_unknown"],
                          "rate":counts[field]/denominator if denominator else None}
        rows.append(row)
    return {"schema_version":1, "groups":rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Local JSON with reviewed runs")
    arguments = parser.parse_args()
    try:
        data = json.loads(arguments.input.read_text(encoding="utf-8-sig"))
        print(json.dumps(summarize(data), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
