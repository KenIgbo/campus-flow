import os
import unittest
from campusflow.storage import (
    tickets,
    save_ticket,
    load_tickets,
)

class TestCampusFlowStorage(unittest.TestCase):

    def setUp(self):
        # Clears the shared storage before every test case run
        tickets.clear()

    def tearDown(self):
        # Safely clean up any persistent storage file created during tests
        # Replace 'tickets.txt' or 'tickets.json' with your actual storage filename if different
        for filename in ["tickets.json", "tickets.txt", "tickets.csv"]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_save_and_load(self):
        tickets.append({
            "id": "T001",
            "title": "Test",
            "category": "network",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "open",
            "assigned_to": None
        })

        save_ticket()

        tickets.clear()

        load_tickets()

        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]["id"], "T001")

    def test_load_no_file(self):
        # Ensure any existing physical save file is gone to force the "no file" state
        for filename in ["tickets.json", "tickets.txt", "tickets.csv"]:
            if os.path.exists(filename):
                os.remove(filename)

        tickets.clear()

        load_tickets()

        self.assertIsInstance(tickets, list)

    def test_save_empty_list(self):
        tickets.clear()

        save_ticket()

        load_tickets()

        self.assertEqual(tickets, [])

if __name__ == "__main__":
    unittest.main()
