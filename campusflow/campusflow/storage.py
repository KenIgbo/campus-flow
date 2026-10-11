import json

tickets = []

def save_ticket():
    with open("tickets.json", "w") as file:
        json.dump(tickets, file, indent=4)


def load_tickets():
    try:
        with open("tickets.json", "r") as file:
            loaded = json.load(file)

        tickets.clear()
        tickets.extend(loaded)

    except (FileNotFoundError, json.JSONDecodeError):
        tickets.clear()