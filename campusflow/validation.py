"""
Centralized validation helpers for CampusFlow Next.

All user-supplied or file-loaded values pass through here BEFORE
any ticket dictionary is mutated. This is "validate-before-mutate".
"""


class ValidationError(Exception):
    """Raised when a value fails a business rule."""
    pass


VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}
VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def validate_title(value):
    if not isinstance(value, str):
        raise ValidationError("Title must be text")
    cleaned = value.strip()
    if cleaned == "":
        raise ValidationError("Title cannot be empty")
    return cleaned


def validate_category(value):
    if not isinstance(value, str):
        raise ValidationError("Category must be text")
    cleaned = value.strip().capitalize()
    if cleaned == "":
        raise ValidationError("Category cannot be empty")
    if cleaned not in VALID_CATEGORIES:
        raise ValidationError(
            f"Category must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )
    return cleaned


def validate_urgency(value):
    if not isinstance(value, str):
        raise ValidationError("Urgency must be text")
    cleaned = value.strip().lower()
    if cleaned == "":
        raise ValidationError("Urgency cannot be empty")
    if cleaned not in VALID_URGENCIES:
        raise ValidationError(
            f"Urgency must be one of: {', '.join(sorted(VALID_URGENCIES))}"
        )
    return cleaned


def validate_affected_users(value):
    """Strictly positive integer. Rejects bools BEFORE the int check."""
    if isinstance(value, bool):
        raise ValidationError("affected_users must be a positive integer")
    if not isinstance(value, int):
        raise ValidationError("affected_users must be a positive integer")
    if value <= 0:
        raise ValidationError("affected_users must be greater than zero")
    return value


def validate_status(value):
    if not isinstance(value, str):
        raise ValidationError("Status must be text")
    cleaned = value.strip().lower()
    if cleaned not in VALID_STATUSES:
        raise ValidationError(
            f"Status must be one of: {', '.join(sorted(VALID_STATUSES))}"
        )
    return cleaned


def validate_priority(value):
    if not isinstance(value, str):
        raise ValidationError("Priority must be text")
    cleaned = value.strip().lower()
    if cleaned not in VALID_PRIORITIES:
        raise ValidationError(
            f"Priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}"
        )
    return cleaned


def validate_staff_label(value):
    if not isinstance(value, str):
        raise ValidationError("Staff name must be text")
    cleaned = value.strip()
    if cleaned == "":
        raise ValidationError("Staff name cannot be empty")
    return cleaned


def validate_ticket_id(value):
    if not isinstance(value, str):
        raise ValidationError("Ticket ID must be text")
    cleaned = value.strip().upper()
    if cleaned == "":
        raise ValidationError("Ticket ID cannot be empty")
    if not cleaned.startswith("T") or not cleaned[1:].isdigit() or len(cleaned) < 4:
        raise ValidationError("Ticket ID must look like T001")
    return cleaned


def validate_note_shape(note):
    if not isinstance(note, dict):
        raise ValidationError("Note must be a dictionary")
    for key in ("note_id", "author", "message"):
        if key not in note:
            raise ValidationError(f"Note is missing field: {key}")

    note_id = note["note_id"]
    if not isinstance(note_id, str):
        raise ValidationError("Note ID must be text")
    note_id = note_id.strip().upper()
    if not note_id.startswith("N") or not note_id[1:].isdigit() or len(note_id) < 4:
        raise ValidationError("Note ID must look like N001")

    author = note["author"]
    if not isinstance(author, str) or author.strip() == "":
        raise ValidationError("Note author cannot be empty")

    message = note["message"]
    if not isinstance(message, str):
        raise ValidationError("Note message must be text")
    message = message.strip()
    if len(message) < 5:
        raise ValidationError("Note message must be at least 5 characters")
    if len(message) > 300:
        raise ValidationError("Note message cannot exceed 300 characters")

    return {
        "note_id": note_id,
        "author": author.strip(),
        "message": message,
    }


def validate_ticket(ticket):
    """Validate a full ticket dict. Raises on any problem. Does not mutate."""
    if not isinstance(ticket, dict):
        raise ValidationError("Ticket must be a dictionary")

    required = (
        "id", "title", "category", "urgency",
        "affected_users", "priority", "status",
        "assigned_to", "notes",
    )
    for key in required:
        if key not in ticket:
            raise ValidationError(f"Ticket is missing field: {key}")

    validate_ticket_id(ticket["id"])
    validate_title(ticket["title"])
    validate_category(ticket["category"])
    validate_urgency(ticket["urgency"])
    validate_affected_users(ticket["affected_users"])
    validate_priority(ticket["priority"])
    validate_status(ticket["status"])

    if ticket["assigned_to"] is not None:
        validate_staff_label(ticket["assigned_to"])

    notes = ticket["notes"]
    if not isinstance(notes, list):
        raise ValidationError("notes must be a list")

    seen = set()
    for note in notes:
        cleaned = validate_note_shape(note)
        if cleaned["note_id"] in seen:
            raise ValidationError(
                f"Duplicate note ID in ticket {ticket['id']}: {cleaned['note_id']}"
            )
        seen.add(cleaned["note_id"])

    return ticket