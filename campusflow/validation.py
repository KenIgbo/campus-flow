"""
Centralized validation helpers for CampusFlow Next.

Every user-supplied or file-loaded value passes through here BEFORE
any ticket dictionary is mutated. This is the "validate-before-mutate"
pattern from the sprint brief (Concept 2).

All functions raise ValidationError on bad input. Callers (CLI or
storage) either catch it and show a message, or let it propagate
when the caller wants the load to abort.
"""


# --------------------------------------------------------------------
# Custom exception
# --------------------------------------------------------------------
class ValidationError(Exception):
    """
    Raised when a value fails a business rule.

    Why a custom class and not plain ValueError?
    - The CLI can catch ONLY our errors and let real bugs propagate.
    - It signals "user error, show a friendly message".
    - Tests can use assertRaises(ValidationError) precisely.
    """
    pass


# --------------------------------------------------------------------
# Canonical value sets (single source of truth)
# --------------------------------------------------------------------
# Stored in Title Case for category (per sprint brief), lower for the rest.
VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}
VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


# --------------------------------------------------------------------
# Field-level validators
# --------------------------------------------------------------------
def validate_title(value):
    """
    Title must be a non-empty string after trimming.

    Returns the cleaned (stripped) title so the caller stores the
    canonical version — never the raw input.
    """
    if not isinstance(value, str):
        raise ValidationError("Title must be text")
    cleaned = value.strip()
    if cleaned == "":
        raise ValidationError("Title cannot be empty")
    return cleaned


def validate_category(value):
    """
    Normalize then check against VALID_CATEGORIES.

    Accepts 'network', 'NETWORK', ' Network ' and stores 'Network'.
    Uses .strip() then .capitalize() so any casing maps to canonical.

    Why capitalize() and not .title()? 'title' would turn 'other' into
    'Other' correctly, but also mangles multi-word names. We only have
    single-word categories, so capitalize() is safer and predictable.
    """
    if not isinstance(value, str):
        raise ValidationError("Category must be text")
    cleaned = value.strip().capitalize()   # 'network' -> 'Network'
    if cleaned == "":
        raise ValidationError("Category cannot be empty")
    if cleaned not in VALID_CATEGORIES:
        raise ValidationError(
            f"Category must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )
    return cleaned


def validate_urgency(value):
    """
    Urgency is stored lowercase: 'low', 'medium', 'high'.
    """
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
    """
    affected_users must be a strictly positive integer.

    THIS IS THE TRICKY ONE. In Python:
        isinstance(True, int)  -> True
        int(True)              -> 1
    So a careless check like `isinstance(value, int) and value > 0`
    would ACCEPT True as a valid count of 1.

    The sprint brief explicitly tests this. We reject bool first.
    We also reject floats and numeric strings — only a real int passes.
    """
    # Reject bool BEFORE the int check, because bool IS a subclass of int.
    if isinstance(value, bool):
        raise ValidationError("affected_users must be a positive integer")
    if not isinstance(value, int):
        raise ValidationError("affected_users must be a positive integer")
    if value <= 0:
        raise ValidationError("affected_users must be greater than zero")
    return value


def validate_status(value):
    """
    Status must be one of: open, in_progress, resolved.
    Stored lowercase.
    """
    if not isinstance(value, str):
        raise ValidationError("Status must be text")
    cleaned = value.strip().lower()
    if cleaned not in VALID_STATUSES:
        raise ValidationError(
            f"Status must be one of: {', '.join(sorted(VALID_STATUSES))}"
        )
    return cleaned


def validate_priority(value):
    """
    Priority must be one of: critical, high, medium, low.
    Stored lowercase.
    """
    if not isinstance(value, str):
        raise ValidationError("Priority must be text")
    cleaned = value.strip().lower()
    if cleaned not in VALID_PRIORITIES:
        raise ValidationError(
            f"Priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}"
        )
    return cleaned


def validate_staff_label(value):
    """
    Assignment label must be non-empty after trimming.
    """
    if not isinstance(value, str):
        raise ValidationError("Staff name must be text")
    cleaned = value.strip()
    if cleaned == "":
        raise ValidationError("Staff name cannot be empty")
    return cleaned


def validate_ticket_id(value):
    """
    Ticket ID must look like T001, T002, ... (T + 3+ digits).
    """
    if not isinstance(value, str):
        raise ValidationError("Ticket ID must be text")
    cleaned = value.strip().upper()
    if cleaned == "":
        raise ValidationError("Ticket ID cannot be empty")
    if not cleaned.startswith("T") or not cleaned[1:].isdigit():
        raise ValidationError("Ticket ID must look like T001")
    return cleaned


# --------------------------------------------------------------------
# Composite validators
# --------------------------------------------------------------------
def validate_note_shape(note):
    """
    A note must be a dict with exactly:
        note_id  -> 'N001' style
        author   -> non-empty string
        message  -> 5..300 chars after trimming

    Used by both add_note() and load_tickets() so the rules are IDENTICAL
    in both entry paths. This is the "single source of truth" idea.
    """
    if not isinstance(note, dict):
        raise ValidationError("Note must be a dictionary")

    for key in ("note_id", "author", "message"):
        if key not in note:
            raise ValidationError(f"Note is missing field: {key}")

    note_id = note["note_id"]
    if not isinstance(note_id, str):
        raise ValidationError("Note ID must be text")
    note_id = note_id.strip().upper()
    if not note_id.startswith("N") or not note_id[1:].isdigit():
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
    """
    Validate a COMPLETE ticket dictionary (the shape stored in JSON).

    Called in two places:
      1. After loading JSON, to reject the whole file if any ticket is bad.
      2. Before saving, as a safety net.

    Returns the ticket unchanged on success, raises on any problem.
    Does NOT modify the caller's dict — pure check.

    Required keys and rules:
      id              -> T### format
      title           -> non-empty
      category        -> Network/Hardware/Software/Other (canonical)
      urgency         -> low/medium/high
      affected_users  -> positive int (bool rejected)
      priority        -> critical/high/medium/low
      status          -> open/in_progress/resolved
      assigned_to     -> None or non-empty string
      notes           -> list of valid notes with unique note_ids
    """
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

    assigned = ticket["assigned_to"]
    if assigned is not None:
        validate_staff_label(assigned)

    notes = ticket["notes"]
    if not isinstance(notes, list):
        raise ValidationError("notes must be a list")

    seen_note_ids = set()
    for note in notes:
        cleaned = validate_note_shape(note)
        if cleaned["note_id"] in seen_note_ids:
            raise ValidationError(
                f"Duplicate note ID in ticket {ticket['id']}: {cleaned['note_id']}"
            )
        seen_note_ids.add(cleaned["note_id"])

    return ticket