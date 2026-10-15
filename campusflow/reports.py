"""
Analytics for the Head of Campus. Engineer B owns this.
"""


def build_report(collection):
    """Return a report dict. Never crashes on empty input."""
    total = len(collection)

    by_status = {"open": 0, "in_progress": 0, "resolved": 0}
    by_priority = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    by_category = {"Network": 0, "Hardware": 0, "Software": 0, "Other": 0}

    for t in collection:
        by_status[t["status"]] = by_status.get(t["status"], 0) + 1
        by_priority[t["priority"]] = by_priority.get(t["priority"], 0) + 1
        by_category[t["category"]] = by_category.get(t["category"], 0) + 1

    resolved = by_status["resolved"]
    unresolved = by_status["open"] + by_status["in_progress"]
    percentage = (resolved / total * 100) if total > 0 else 0.0

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "unresolved": unresolved,
        "resolved": resolved,
        "resolution_percentage": percentage,
    }


def view_reports(collection=None):
    if collection is None:
        from campusflow.storage import tickets as collection
    r = build_report(collection)
    print("=" * 40 + " REPORTS " + "=" * 40)
    print(f"Total tickets: {r['total']}")
    print("\nBy Status:")
    for k, v in r["by_status"].items():
        print(f"  {k}: {v}")
    print("\nBy Priority:")
    for k, v in r["by_priority"].items():
        print(f"  {k}: {v}")
    print("\nBy Category:")
    for k, v in r["by_category"].items():
        print(f"  {k}: {v}")
    print(f"\nUnresolved (open + in_progress): {r['unresolved']}")
    print(f"Resolved: {r['resolved']}")
    print(f"Resolution: {r['resolution_percentage']:.1f}%")