import io
import unittest
from unittest.mock import patch, mock_open
from campusflow.storage import (
    tickets,
    save_ticket,
    load_tickets,
)

class TestCampusFlowStorage(unittest.TestCase):

    def setUp(self):
        # Clears the shared storage before every test case run
        tickets.clear()
        
        # Start a global patch on 'open' so no test writes to disk
        # We start with an empty file state ""
        self.mock_file = mock_open(read_data="")
        self.file_patcher = patch("builtins.open", self.mock_file)
        self.file_patcher.start()

    def tearDown(self):
        # Stop the patcher to clean up after each test
        self.file_patcher.stop()

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

        # When save_ticket writes, it goes into our mocked file system
        save_ticket()

        # Gather what was written to simulate a persistent file for the load step
        written_data = "".join(call.args[0] for call in self.mock_file().write.call_args_list)
        
        # Update the mock so the next 'open' read returns what we just saved
        self.mock_file.return_value.read.return_value = written_data

        tickets.clear()
        load_tickets()

        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]["id"], "T001")

    def test_load_no_file(self):
        # Simulate "file not found" by forcing open() to raise a FileNotFoundError
        self.mock_file.side_effect = FileNotFoundError

        tickets.clear()
        load_tickets()

        self.assertIsInstance(tickets, list)

    def test_save_empty_list(self):
        tickets.clear()
        save_ticket()

        # Update mock read stream with the empty file state output
        written_data = "".join(call.args[0] for call in self.mock_file().write.call_args_list)
        self.mock_file.return_value.read.return_value = written_data

        load_tickets()
        self.assertEqual(tickets, [])

if __name__ == "__main__":
    unittest.main()
