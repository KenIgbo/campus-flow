from campusflow.storage import tickets, save_ticket

def update_status():
    status_list = ["open", "in_progress", "resolved"]
    ticket_id = input("Enter Ticket ID: ")
    
    if ticket_id.strip() == "":
        return "Ticket ID cannot be empty"

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            status = input("Enter new status: ")

            if status.strip() == "":
                return "Status cannot be empty"

            status_lower = status.lower()

            if status_lower not in status_list:
                return "Status not supported"

            if ticket["assigned_to"] == None:
                return "Update rejected"
            else:
                if ticket["status"] == "open":
                    if status_lower == "open":
                        return "Status already 'open'"
                    elif status_lower == "resolved":
                        return "Update rejected"
                    else:
                        ticket["status"] = status_lower
                        save_ticket()
                        return "Status updated"

                elif ticket["status"] == "in_progress":
                    if status_lower == "open":
                        return "Update rejected"
                    elif status_lower == "in_progress":
                        return "Status already 'in_progress'"
                    else:
                        ticket["status"] = status_lower
                        save_ticket()
                        return "Status updated"

                else:
                    if status_lower == "resolved":
                        return "Status already 'resolved'"
                    elif status_lower == "in_progress":
                        return "Update rejected"
                    else:
                        ticket["status"] = status_lower
                        save_ticket()
                        return "Status updated"

    return "Ticket ID not found"


def work_queue():
    headings = [["ID", "TITLE", "CATEGORY", "URGENCY", "AFFECTED USERS", "PRIORITY", "STATUS", "ASSIGNED TO"]]
    queue = []
    for ticket in tickets:
        if ticket["priority"] == "critical":
            if ticket["status"] != "resolved":
                queue.append(ticket)

    for ticket in tickets:
        if ticket["priority"] == "high":
            if ticket["status"] != "resolved":
                queue.append(ticket)

    for ticket in tickets:
        if ticket["priority"] == "medium":
            if ticket["status"] != "resolved":
                queue.append(ticket)

    for ticket in tickets:
        if ticket["priority"] == "low":
            if ticket["status"] != "resolved":
                queue.append(ticket)

    for i in range(len(queue)):
        add = []
        for key in queue[i]:
            add.append(queue[i][key])
        headings.append(add)

    print("======================================================= WORK QUEUE =======================================================\n")
    col_widths = [max(len(str(item)) for item in col) for col in zip(*headings)]

    for row in headings:
        formatted_row = " | ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row))
        print(formatted_row)