from campusflow.storage import tickets, save_ticket

def gen_id():
    if len(tickets) == 0:
        id_val = "1"
        id_val_str = "T00" + id_val

    else:
        last_ticket = tickets[-1]
        id_val = last_ticket["id"][3:]
        id_val_str = "T00" + str(int(id_val)+1)

    return id_val_str


def note_id():
    if len(target_ticket) == 0:
        id_val = "1"
        id_val_str = "N00" + id_val

    else:
        last_note = target_ticket["notes"][-1]
        id_val = last_note["note_id"][3:]
        id_val_str = "N00" + str(int(id_val)+1)

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
    headings = [["ID", "TITLE", "CATEGORY", "URGENCY", "AFFECTED USERS", "PRIORITY", "STATUS", "ASSIGNED TO"]]
    for i in range(len(tickets)):
        add = []
        for key in tickets[i]:
            add.append(tickets[i][key])
        headings.append(add)

    col_widths = [max(len(str(item)) for item in col) for col in zip(*headings)]

    print("======================================================= TICKETS LIST =======================================================\n")
    for row in headings:
        formatted_row = " | ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row)) # {item:<{width}} left-aligns the text within the calculated column width
        print(formatted_row)


def view_ticket():
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
                   return "Author name cannot be blank"
                
                message = input("Enter note message: ").strip()
                if message == "":
                   return "message cannot be blank"
                
                if len(message)<5 or len(message)>300:
                   return "message must contain 5-300 characters"
                
            else:
                return "A resolved ticket cannot accept a new note"  
                
            target_ticket["notes"].append({"note_id":note_id(), "author":author, "message":message})
            save_ticket()
            return "Note added sucessfully"
    
    return "ID not found"


def view_ticket_notes():
    ticket_id = input("Enter ticket ID: ")
    if ticket_id.strip() == "":
        print("Ticket ID cannot be empty")
        return
    
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            list_2d = [["NOTE ID", "AUTHOR", "MESSAGE"]]
            for i in range(len(ticket["notes"])):
                add = []
                for key in ticket["notes"][i]:
                    add.append(ticket["notes"][i][key])
                list_2d.append(add)

            col_widths = [max(len(str(item)) for item in col) for col in zip(*list_2d)]

            print(f"====================================================== {ticket_id} NOTES ========================================================\n")
            for row in list_2d:
                formatted_row = " | ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row))
                print(formatted_row)
            return
                    
    print("ID not found")
    return

     

    