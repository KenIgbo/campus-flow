# import json

# tickets = []

# def save_ticket():
#     with open("tickets.json", "w") as file:
#         json.dump(tickets, file, indent=4)


# def load_tickets():
#     try:
#         with open("tickets.json", "r") as file:
#             loaded = json.load(file)

#         tickets.clear()
#         tickets.extend(loaded)

#     except (FileNotFoundError, json.JSONDecodeError):
#         tickets.clear()


"""
Storage layer: in-memory tickets list + safe JSON load/save.

Key guarantees:
- load_tickets validates the WHOLE file before touching memory.
- If anything is wrong, memory is left untouched.
- next_ticket_id / next_note_id never collide, even after reload.
"""

import json
import os

from campusflow.validation import (
    ValidationError,
    validate_ticket,
)


# In-memory collection — shared by every module that imports it.
tickets = []


# Default file path (repo root)
DEFAULT_PATH = "tickets.json"


# ---------------------------------------------------------------------
# ID generation (collision-safe)
# ---------------------------------------------------------------------
def next_ticket_id(collection=None):
    """
    Return the next T### ID by looking at the MAX id in the collection.

    Why not use tickets[-1]? Because the list may be reordered, entries
    may be deleted, or IDs may be non-contiguous after a reload.
    Scanning for the max is O(n) but guaranteed correct.
    """
    if collection is None:
        collection = tickets
    max_num = 0
    for t in collection:
        tid = t.get("id", "")
        if isinstance(tid, str) and tid.startswith("T") and tid[1:].isdigit():
            n = int(tid[1:])
            if n > max_num:
                max_num = n
    return f"T{max_num + 1:03d}"


def next_note_id(ticket):
    """
    Return the next N### ID for a specific ticket.
    """
    max_num = 0
    for note in ticket.get("notes", []):
        nid = note.get("note_id", "")
        if isinstance(nid, str) and nid.startswith("N") and nid[1:].isdigit():
            n = int(nid[1:])
            if n > max_num:
                max_num = n
    return f"N{max_num + 1:03d}"


# ---------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------
def save_tickets(path=DEFAULT_PATH, collection=None):
    """
    Save the ticket collection to a JSON file.

    Writes to a temp file first, then atomically replaces the target.
    This prevents a half-written file if the program crashes mid-save.
    """
    if collection is None:
        collection = tickets

    for ticket in collection:
        validate_ticket(ticket)

    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=4)
    os.replace(tmp_path, path)


# Backwards-compatible alias (old code calls save_ticket()).
def save_ticket():
    save_tickets()


# ---------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------
def load_tickets(path=DEFAULT_PATH, collection=None):
    """
    Load tickets from JSON and REPLACE the in-memory list only on success.

    - FileNotFoundError -> leave memory alone, do nothing.
    - JSONDecodeError   -> raise ValidationError("corrupt file").
    - Any ticket fails validate_ticket -> raise ValidationError.
    - Duplicate ticket IDs -> raise ValidationError.

    On any error, the existing in-memory list is UNCHANGED.
    """
    if collection is None:
        collection = tickets

    if not os.path.exists(path):
        return  # first run — nothing to load

    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Corrupt JSON file: {e}")

    if not isinstance(loaded, list):
        raise ValidationError("JSON file must contain a list of tickets")

    seen_ids = set()
    for ticket in loaded:
        validate_ticket(ticket)
        tid = ticket["id"]
        if tid in seen_ids:
            raise ValidationError(f"Duplicate ticket ID: {tid}")
        seen_ids.add(tid)

    # Passed all checks — safe to swap in.
    collection.clear()
    collection.extend(loaded)