"""
Read-only search with combined filters. Engineer B owns this.
"""

from campusflow.validation import (
    ValidationError,
    validate_category,
    validate_status,
    validate_priority,
)


def search_tickets(title_substring="", category=None, status=None,
                   priority=None, collection=None):
    """
    Return a list of tickets matching ALL supplied filters.

    - title_substring: case-insensitive substring match (casefold)
    - category/status/priority: exact match after normalization
    - None or "" means "do not filter by this field"
    - Does NOT modify collection.
    """
    if collection is None:
        from campusflow.storage import tickets as collection

    needle = title_substring.strip().casefold()

    cat_norm = status_norm = prio_norm = None
    if category:
        cat_norm = validate_category(category)
    if status:
        status_norm = validate_status(status)
    if priority:
        prio_norm = validate_priority(priority)

    results = []
    for t in collection:
        if needle and needle not in t["title"].casefold():
            continue
        if cat_norm and t["category"] != cat_norm:
            continue
        if status_norm and t["status"] != status_norm:
            continue
        if prio_norm and t["priority"] != prio_norm:
            continue
        results.append(t)

    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    results.sort(key=lambda t: (priority_order[t["priority"]], int(t["id"][1:])))
    return results