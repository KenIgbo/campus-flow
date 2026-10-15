from campusflow.storage import load_tickets, tickets
from campusflow.tickets import (
    create_ticket_cli, assign_ticket_cli, list_tickets, view_ticket_cli,
)
from campusflow.workflow import update_status, work_queue
from campusflow.reports import view_reports
from campusflow.search import search_tickets
from campusflow.notes import add_note, get_notes
from campusflow.understanding_check import run_check
from campusflow.validation import ValidationError


def menu_search():
    title = input("Title substring (blank = any): ").strip()
    cat = input("Category (blank = any): ").strip() or None
    st = input("Status (blank = any): ").strip() or None
    pr = input("Priority (blank = any): ").strip() or None
    try:
        results = search_tickets(title, cat, st, pr)
    except ValidationError as e:
        print(f"Error: {e}")
        return
    if not results:
        print("(no matches)")
        return
    for t in results:
        print(f"{t['id']} | {t['title']} | {t['category']} | "
              f"{t['priority']} | {t['status']} | {t['assigned_to']}")


def menu_add_note():
    tid = input("Ticket ID: ").strip()
    author = input("Author: ").strip()
    message = input("Message: ").strip()
    try:
        note = add_note(tid, author, message)
        print(f"Note {note['note_id']} added.")
    except ValidationError as e:
        print(f"Error: {e}")


def menu_view_notes():
    tid = input("Ticket ID: ").strip()
    try:
        notes = get_notes(tid)
        if not notes:
            print("(no notes)")
            return
        for n in notes:
            print(f"{n['note_id']} | {n['author']} | {n['message']}")
    except ValidationError as e:
        print(f"Error: {e}")


def menu():
    print("\n========== CAMPUSFLOW NEXT ==========")
    print("1.  Add Ticket")
    print("2.  Assign Ticket")
    print("3.  Update Status")
    print("4.  List Tickets")
    print("5.  View Ticket")
    print("6.  Open Work Queue")
    print("7.  Reports")
    print("8.  Search Tickets")
    print("9.  Add Follow-up Note")
    print("10. View Ticket Notes")
    print("11. Engineering Understanding Check")
    print("12. Exit")

    choice = input("Select an option: ").strip()

    if choice == "1":
        print(create_ticket_cli())
    elif choice == "2":
        print(assign_ticket_cli())
    elif choice == "3":
        print(update_status())
    elif choice == "4":
        list_tickets()
    elif choice == "5":
        print(view_ticket_cli())
    elif choice == "6":
        work_queue()
    elif choice == "7":
        view_reports()
    elif choice == "8":
        menu_search()
    elif choice == "9":
        menu_add_note()
    elif choice == "10":
        menu_view_notes()
    elif choice == "11":
        run_check()
    elif choice == "12":
        return False
    else:
        print("Unknown option")
    return True


def main():
    try:
        load_tickets()
    except ValidationError as e:
        print(f"Warning: could not load tickets.json — {e}")
        print("Starting with empty in-memory list. File was NOT modified.")
    while True:
        if not menu():
            break


if __name__ == "__main__":
    main()