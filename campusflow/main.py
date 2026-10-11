from campusflow.storage import load_tickets
from campusflow.tickets import (
    create_ticket,
    assign_ticket,
    list_tickets,
    view_ticket
)
from campusflow.workflow import (
    update_status,
    work_queue
)
from campusflow.reports import view_reports


def menu():
    print("\n======================================================= CAMPUS FLOW =======================================================")
    print("1.  Add Ticket\n2.  Assign Ticket\n3.  Update Status\n4.  List Tickets\n5.  View Ticket\n6.  View Work Queue\n7.  View Report\n8.  Exit\n")
    option = input("Select an option: ")

    if option == "1":
        print(create_ticket())
    elif option == "2":
        print(assign_ticket())
    elif option == "3":
        print(update_status())
    elif option == "4":
        list_tickets()
    elif option == "5":
        print(view_ticket())
    elif option == "6":
        work_queue()
    elif option == "7":
        view_reports()
    elif option == "8":
        exit()
    else:
        print("Unknown option")
        return


load_tickets()

while True:
    menu()