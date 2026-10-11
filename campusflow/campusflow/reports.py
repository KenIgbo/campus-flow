from campusflow.storage import tickets

def view_reports():
    num_of_tickets = len(tickets)
    if num_of_tickets == 0:
        print("======================================================= TICKET REPORTS =======================================================\n")
        print("Total tickets: 0\n\nBy Status:\nOpen: 0\nIn Progress: 0\nResolved: 0\n\nBy Priority:\nCritical: 0\nHigh: 0\nMedium: 0\nLow: 0")

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

        print("======================================================= TICKET REPORTS =======================================================\n")
        print(f"Total tickets: {num_of_tickets}\n\nBy Status:\nOpen: {num_open}\nIn Progress: {num_inprogess}\nResolved: {num_resolved}\n\nBy Priority:\nCritical: {num_critical}\nHigh: {num_high}\nMedium: {num_medium}\nLow: {num_low}")
