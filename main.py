from campusflow.storage import load_tickets
from campusflow.tickets import (
    create_ticket,
    assign_ticket,
    list_tickets,
    view_ticket,
    add_note,
    view_ticket_notes,
)

from campusflow.workflow import (
    update_status,
    work_queue
)

from campusflow.reports import view_reports, search_tickets


def menu():
    print("\n======================================================= CAMPUS FLOW =======================================================")
    print("1.   Add Ticket\n2.   Assign Ticket\n3.   Update Status\n4.   List Tickets\n5.   View Ticket\n6.   View Work Queue\n7.   View Report\n8.   Add Note\n9.   View Ticket Notes\n10.  Search Tickets\n11.  Exit\n")
    option = input("Select an option: ")

    if option.strip() == "":
        print("Empty option... try again")
    elif option.strip() == "1":
        print(create_ticket())
    elif option.strip() == "2":
        print(assign_ticket())
    elif option.strip() == "3":
        print(update_status())
    elif option.strip() == "4":
        list_tickets()
    elif option.strip() == "5":
        print(view_ticket())
    elif option.strip() == "6":
        work_queue()
    elif option.strip() == "7":
        view_reports()
    elif option.strip() == "8":
        print(add_note())
    elif option.strip() == "9":
        view_ticket_notes()
    elif option.strip() == "10":
        search_tickets()
        # print(search_tickets())
    elif option.strip() == "11":
        exit()
    else:
        print("Unknown option")
        return


load_tickets()

while True:
    menu()