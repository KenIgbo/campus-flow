"""
Note data layer. Owned by Engineer A.
"""

from campusflow.validation import (
    ValidationError,
    validate_ticket_id,
    validate_staff_label,
)
from campusflow.storage import tickets, save_ticket, next_note_id


def _find_ticket(ticket_id, collection=None):
    if collection is None:
        collection = tickets
    tid = validate_ticket_id(ticket_id)
    for t in collection:
        if t["id"] == tid:
            return t
    raise ValidationError(f"Ticket {tid} not found")


def add_note(ticket_id, author, message, collection=None):
    """
    Add a structured note to an open or in_progress ticket.

    Rules:
    - status must be open or in_progress
    - author non-empty
    - message 5..300 chars after trimming
    - a rejected note must NOT consume a note ID
    - a failed action must leave the ticket unchanged

    Returns the created note dict.
    """
    if collection is None:
        collection = tickets

    ticket = _find_ticket(ticket_id, collection)

    if ticket["status"] == "resolved":
        raise ValidationError(
            "Cannot add a note to a resolved ticket. Reopen it first."
        )

    author_clean = validate_staff_label(author)

    if not isinstance(message, str):
        raise ValidationError("Note message must be text")
    message_clean = message.strip()
    if len(message_clean) < 5:
        raise ValidationError("Note message must be at least 5 characters")
    if len(message_clean) > 300:
        raise ValidationError("Note message cannot exceed 300 characters")

    # Only NOW do we compute the ID and mutate.
    note_id = next_note_id(ticket)
    note = {
        "note_id": note_id,
        "author": author_clean,
        "message": message_clean,
    }
    ticket.setdefault("notes", [])
    ticket["notes"].append(note)
    save_ticket()
    return note


def get_notes(ticket_id, collection=None):
    """Return the ticket's notes sorted by note_id."""
    ticket = _find_ticket(ticket_id, collection)
    return sorted(ticket.get("notes", []), key=lambda n: n["note_id"])