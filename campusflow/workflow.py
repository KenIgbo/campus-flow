"""
Status transitions and priority calculation. Engineer A owns the rules,
Engineer B owns the CLI wrapper.
"""

from campusflow.storage import tickets, save_ticket
from campusflow.validation import (
    ValidationError,
    validate_ticket_id,
    validate_status,
    validate_staff_label,
)


# Legal transitions: current -> {allowed nexts}
TRANSITIONS = {
    "open":        {"in_progress"},
    "in_progress": {"resolved"},
    "resolved":    {"open"},   # reopen
}


def can_transition(current, target):
    """
    Return True if moving current -> target is legal.
    Pure function — no side effects. Easy to test.
    """
    current = (current or "").strip().lower()
    target = (target or "").strip().lower()
    return target in TRANSITIONS.get(current, set())


def _find_ticket(ticket_id, collection=None):
    if collection is None:
        collection = tickets
    tid = validate_ticket_id(ticket_id)
    for t in collection:
        if t["id"] == tid:
            return t
    raise ValidationError(f"Ticket {tid} not found")


def change_status(ticket_id, new_status, collection=None):
    """
    Business-layer status change. Raises ValidationError on any rule break.
    Does NOT read from input() — CLI does that separately.
    """
    if collection is None:
        collection = tickets

    ticket = _find_ticket(ticket_id, collection)
    target = validate_status(new_status)
    current = ticket["status"]

    if current == target:
        raise ValidationError(f"Status is already '{current}'")

    if not can_transition(current, target):
        raise ValidationError(f"Cannot change status from '{current}' to '{target}'")

    # Business rule from the brief: an unassigned ticket cannot start work.
    if target == "in_progress" and ticket["assigned_to"] is None:
        raise ValidationError("Ticket must be assigned before starting work")

    ticket["status"] = target
    save_ticket()
    return ticket


def calculate_priority(urgency, affected_users):
    """
    Priority rule (order matters — preserved from original CampusFlow):
      critical: high urgency AND users >= 10
      high:     high urgency OR  users >= 10
      medium:   medium urgency OR users >= 3
      low:      otherwise
    """
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


# ---------------------------------------------------------------------
# CLI-facing wrappers (Engineer B uses these; kept here for compat)
# ---------------------------------------------------------------------
def update_status():
    """Interactive status update. Returns a message string."""
    tid = input("Enter Ticket ID: ").strip()
    if tid == "":
        return "Ticket ID cannot be empty"
    try:
        new_status = input("Enter new status: ").strip()
        if new_status == "":
            return "Status cannot be empty"
        ticket = change_status(tid, new_status)
        return f"Status updated to '{ticket['status']}' successfully"
    except ValidationError as e:
        return str(e)


def work_queue():
    """
    Open Work Queue — ORIGINAL behaviour.
    Only OPEN tickets. Priority critical > high > medium > low.
    Ties: earlier numeric ticket ID first.
    """
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    queue = [t for t in tickets if t["status"] == "open"]
    queue.sort(key=lambda t: (priority_order.get(t["priority"], 9), int(t["id"][1:])))

    headings = [["ID", "TITLE", "CATEGORY", "PRIORITY", "STATUS", "ASSIGNED TO"]]
    for t in queue:
        headings.append([
            t["id"], t["title"], t["category"],
            t["priority"], t["status"], str(t["assigned_to"]),
        ])

    print("=" * 50 + " WORK QUEUE " + "=" * 50)
    if len(headings) == 1:
        print("(no open tickets)")
        return
    col_widths = [max(len(str(row[i])) for row in headings) for i in range(len(headings[0]))]
    for row in headings:
        print(" | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)))