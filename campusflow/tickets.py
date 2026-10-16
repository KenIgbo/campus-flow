from campusflow.storage import tickets, save_ticket

def gen_id():
    if len(tickets) == 0:
        id_val = "1"
        id_val_str = "T00" + id_val
    else:
        id_list = [int(str(ticket["id"][3:])) for ticket in tickets]
        max_id = max(id_list)
        id_val_str = "T00" + str(max_id + 1)
    return id_val_str
        


def note_id():
    if len(target_ticket["notes"]) == 0:
        id_val = "1"
        id_val_str = "N00" + id_val

    else:
        note_id_list = [int(str(note["note_id"][3:])) for note in target_ticket["notes"]]
        max_note_id = max(note_id_list)
        id_val_str = "N00" + str(max_note_id + 1)

    return id_val_str


def cal_priority():
    if urgency == "high" and affected_users_val >= 10:
        return "critical"
    elif urgency == "high" or affected_users_val >= 10:
        return "high"
    elif urgency == "medium" or affected_users_val >= 3:
        return "medium"
    else:
        return "low"


def create_ticket():
    global urgency
    global affected_users_val

    cat_list = ["network", "hardware", "software", "other"]
    urgency_list = ["low", "medium", "high"]

    title = input("Enter title: ")
    if title.strip() == "":
        return "Title cannot be empty"

    cat = input("Enter category: ")
    if cat.strip() == "":
        return "Category cannot be empty"
    if cat.lower() not in cat_list:
        return "Category not supported"

    urgency = input("Enter urgency: ")
    if urgency.strip() == "":
        return "Urgency cannot be empty"
    if urgency.lower() not in urgency_list:
        return "Urgency not supported"

    affected_users = input("Enter number of affected users: ")
    try:
        affected_users_val = int(affected_users)
    except ValueError:
        return "Input must be a whole number"

    if affected_users_val <= 0:
        return "Input must be greater than zero"

    ticket = {
        "id": gen_id(), 
        "title": title.capitalize(), 
        "category": cat.lower(), 
        "urgency": urgency.lower(), 
        "affected_users": affected_users_val, 
        "priority": cal_priority(), 
        "status": "open", 
        "assigned_to": None,
        "notes": []
    }

    tickets.append(ticket)
    save_ticket()

    return "Ticket created successfully\n"


def assign_ticket():
    if len(tickets) == 0:
        return "No ticket recorded"

    ticket_id = input("Enter Ticket ID: ")

    if ticket_id.strip() == "":
        return "Ticket ID cannot be empty"

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["status"] == "resolved":
                return "Cannot reassign a resolved ticket"
            
            name = input("Enter Staff Name: ")
            if name.strip() == "":
                return "Name cannot be empty"

            ticket["assigned_to"] = name
            save_ticket()

            return f"{ticket_id} assigned to {name} successfully"

    return "Ticket ID not found"


def list_tickets():
    if len(tickets) == 0:
        print("No ticket recorded")
        return

    headings = [["ID", "TITLE", "CATEGORY", "URGENCY", "AFFECTED USERS", "PRIORITY", "STATUS", "ASSIGNED TO"]]
    for ticket in tickets:
        add = [ticket["id"], ticket["title"], ticket["category"], ticket["urgency"], ticket["affected_users"], ticket["priority"], ticket["status"], ticket["assigned_to"]]
        headings.append(add)

    col_widths = [max(len(str(item)) for item in col) for col in zip(*headings)]

    print("======================================================= TICKETS LIST =======================================================\n")
    for row in headings:
        formatted_row = " | ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row)) # {item:<{width}} left-aligns the text within the calculated column width
        print(formatted_row)


def view_ticket():
    if len(tickets) == 0:
        return "No ticket recorded"

    ticket_id = input("Enter Ticket ID: ")
    if ticket_id.strip() == "":
        return "Ticket ID cannot be empty"

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            max_key_len = max(len(str(key)) for key in ticket)
            lines = [f"{key.capitalize():<{max_key_len}} : {str(value)}" for key, value in ticket.items()]

            return f"======================================================= DETAILS OF {ticket_id} =======================================================\n" + "\n".join(lines)
    return "ID not found"
    

def add_note():
    if len(tickets) == 0:
        return "No ticket recorded"

    global target_ticket

    ticket_id = input("Enter Ticket ID: ")    
    if ticket_id.strip() == "":
        return "Ticket ID cannot be empty"
    
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            target_ticket = ticket

            if target_ticket["assigned_to"] == None:
                return "Update rejected! ticket not assigned"
            
            if target_ticket["status"] == "open" or target_ticket["status"] == "in_progress":

                author = input("Enter author name: ").strip()
                if author == "":
                   return "Author name cannot be empty"
                
                message = input("Enter note message: ").strip()
                if message == "":
                   return "Message cannot be empty"
                
                if len(message)<5 or len(message)>300:
                   return "Message must contain 5-300 characters"
                
            else:
                return "A resolved ticket cannot accept a new note"  
                
            target_ticket["notes"].append({"note_id":note_id(), "author":author, "message":message})
            save_ticket()
            return "Note added sucessfully"
    
    return "ID not found"


def view_ticket_notes():
    if len(tickets) == 0:
        print("No ticket recorded")
        return

    ticket_id = input("Enter ticket ID: ")
    if ticket_id.strip() == "":
        print("Ticket ID cannot be empty")
        return
    
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["notes"] == []:
                print("No notes for this Ticket")
                return

            list_2d = [["NOTE ID", "AUTHOR", "MESSAGE"]]
            for note in ticket["notes"]:
                add = [note["note_id"], note["author"], note["message"]]
                list_2d.append(add)

            col_widths = [max(len(str(item)) for item in col) for col in zip(*list_2d)]

            print(f"====================================================== {ticket_id} NOTES ========================================================\n")
            for row in list_2d:
                formatted_row = " | ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row))
                print(formatted_row)
            return
                    
    print("ID not found")
    return

     

    