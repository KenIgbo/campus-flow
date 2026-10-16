from campusflow.storage import tickets

def view_reports():
    num_of_tickets = len(tickets)

    if num_of_tickets == 0:
        print("======================================================= TICKET REPORTS =======================================================\n")
        print("Total tickets: 0\n\nBy Status:\nOpen: 0\nIn Progress: 0\nResolved: 0\n\nBy Priority:\nCritical: 0\nHigh: 0\nMedium: 0\nLow: 0\n\nBy Category:\nNetwork: 0\nHardware: 0\nSoftware: 0\nOther: 0\n\nUnresolved: 0\n\nResolved: 0\n\nResolution percentage: 0%")

    else:
        num_open = 0
        for ticket in tickets:
            if ticket["status"] == "open":
                num_open += 1

        num_inprogess = 0
        for ticket in tickets:
            if ticket["status"] == "in_progress":
                num_inprogess += 1

        num_resolved = 0
        for ticket in tickets:
            if ticket["status"] == "resolved":
                num_resolved += 1

        num_critical = 0
        for ticket in tickets:
            if ticket["priority"] == "critical":
                num_critical += 1

        num_high = 0
        for ticket in tickets:
            if ticket["priority"] == "high":
                num_high += 1

        num_medium = 0
        for ticket in tickets:
            if ticket["priority"] == "medium":
                num_medium += 1

        num_low = 0
        for ticket in tickets:
            if ticket["priority"] == "low":
                num_low += 1

        num_network = 0
        for ticket in tickets:
            if ticket["category"] == "network":
                num_network += 1

        num_hardware = 0
        for ticket in tickets:
            if ticket["category"] == "hardware":
                num_hardware += 1

        num_software = 0
        for ticket in tickets:
            if ticket["category"] == "software":
                num_software += 1

        num_other = 0
        for ticket in tickets:
            if ticket["category"] == "other":
                num_other += 1


        num_unresolved = num_open + num_inprogess
        resolution_percent = (num_resolved/num_of_tickets) * 100
        rounded = round(resolution_percent, 2)

        print("======================================================= TICKET REPORTS =======================================================\n")
        print(f"Total tickets: {num_of_tickets}\n\nBy Status:\nOpen: {num_open}\nIn Progress: {num_inprogess}\nResolved: {num_resolved}\n\nBy Priority:\nCritical: {num_critical}\nHigh: {num_high}\nMedium: {num_medium}\nLow: {num_low}\n\nBy Category:\nNetwork: {num_network}\nHardware: {num_hardware}\nSoftware: {num_software}\nOther: {num_other}\n\nUresolved: {num_unresolved}\n\nResolved: {num_resolved}\n\nResolution percentage: {rounded}%")


def search_tickets():
    if len(tickets) == 0:
        print("No ticket recorded")
        return

    cat_list = ["network", "hardware", "software", "other"]
    status_list = ["open", "in_progress", "resolved"]
    prio_list = ["critical", "high", "medium", "low"]

    check = []

    title = input("Enter title: ").strip().lower()
    if title == "":
        print("Title cannot be empty")
        return

    while True:
        cat = input("Enter category: ").strip().lower()
        if cat == "":
            break
        if cat in cat_list:
            check.append(cat)
            break
        print("Category not supported")

    while True:
        status = input("Enter status: ").strip().lower()
        if status == "":
            break
        if status in status_list:
            check.append(status)
            break
        print("Status not supported")

    while True:
        priority = input("Enter priority: ").strip().lower()
        if priority == "":
            break
        if priority in prio_list:
            check.append(priority)
            break
        print("Priority not supported")

    headings = [["ID", "TITLE", "CATEGORY", "PRIORITY", "STATUS", "ASSIGNED TO"]]

    for ticket in tickets:
        if title in ticket["title"].lower():
            cnt = 0
            for key in ticket:
                if ticket[key] in check:
                    cnt += 1
            if cnt == len(check):
                add = [ticket["id"], ticket["title"], ticket["category"], ticket["priority"], ticket["status"], ticket["assigned_to"]]

                headings.append(add)

    if len(headings) == 1:
        print("\nNo match found")
        return

    col_widths = [max(len(str(item)) for item in col) for col in zip(*headings)]

    print(f"====================================================== MATCHES ========================================================\n")
    for row in headings:
        formatted_row = " | ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row))
        print(formatted_row)