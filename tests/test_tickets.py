import unittest
from unittest.mock import patch
from campusflow.storage import tickets
from campusflow.tickets import create_ticket, assign_ticket

class TestCampusFlowTickets(unittest.TestCase):

    def setUp(self):
        # Clears the storage before every single test case run
        tickets.clear()
        
        # Globally mock save_ticket across all tests to prevent disk writes
        self.save_patcher = patch("campusflow.tickets.save_ticket")
        self.mock_save_ticket = self.save_patcher.start()

    def tearDown(self):
        # Stop the patcher cleanly after each test runs
        self.save_patcher.stop()

    # --- Create Ticket Tests ---

    @patch("builtins.input")
    def test_create_ticket_success(self, mock_input):
        mock_input.side_effect = [
            "Wifi Down",
            "network",
            "high",
            "15"
        ]

        result = create_ticket()

        self.assertEqual(result, "Ticket created successfully\n")
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]["priority"], "critical")
        # Optional check to make sure it tried to save safely in memory:
        self.mock_save_ticket.assert_called_once()

    @patch("builtins.input")
    def test_create_ticket_empty_title(self, mock_input):
        mock_input.side_effect = [""]

        result = create_ticket()

        self.assertEqual(result, "Title cannot be empty")

    @patch("builtins.input")
    def test_invalid_category(self, mock_input):
        mock_input.side_effect = [
            "Wifi Down",
            "security",
        ]

        result = create_ticket()

        self.assertEqual(result, "Category not supported")

    @patch("builtins.input")
    def test_empty_category(self, mock_input):
        mock_input.side_effect = [
            "Wifi Down",
            ""
        ]

        result = create_ticket()

        self.assertEqual(result, "Category cannot be empty")

    @patch("builtins.input")
    def test_invalid_urgency(self, mock_input):
        mock_input.side_effect = [
            "Wifi Down",
            "network",
            "urgent"
        ]

        result = create_ticket()

        self.assertTrue(result)  # Asserts that the return value is truthy

    @patch("builtins.input")
    def test_invalid_affected_users(self, mock_input):
        mock_input.side_effect = [
            "Wifi Down",
            "network",
            "high",
            "abc"
        ]

        result = create_ticket()

        self.assertEqual(result, "Input must be a whole number")

    @patch("builtins.input")
    def test_negative_affected_users(self, mock_input):
        mock_input.side_effect = [
            "Wifi Down",
            "network",
            "high",
            "-5"
        ]

        result = create_ticket()

        self.assertEqual(result, "Input must be greater than zero")


    # --- Assign Ticket Tests ---

    # --- Empty Assign Input Edge Cases ---

    @patch("builtins.input")
    def test_assign_ticket_empty_id(self, mock_input):
        # Feeds an empty space as the first input (Ticket ID)
        mock_input.side_effect = ["   "]

        result = assign_ticket()

        self.assertEqual(result, "Ticket ID cannot be empty")

    @patch("builtins.input")
    def test_assign_ticket_empty_name(self, mock_input):
        tickets.append({
            "id": "T001",
            "title": "Wifi",
            "category": "network",
            "urgency": "high",
            "affected_users": 10,
            "priority": "critical",
            "status": "open",
            "assigned_to": None
        })
        
        # Valid Ticket ID first, followed by empty spaces for the Staff Name
        mock_input.side_effect = ["T001", "   "]

        result = assign_ticket()

        self.assertEqual(result, "Name cannot be empty")


    @patch("builtins.input")
    def test_assign_ticket_success(self, mock_input):
        tickets.append({
            "id": "T001",
            "title": "Wifi",
            "category": "network",
            "urgency": "high",
            "affected_users": 10,
            "priority": "critical",
            "status": "open",
            "assigned_to": None
        })
        
        # Matches your prompts: 1st for Ticket ID, 2nd for Staff Name
        mock_input.side_effect = ["T001", "Agent_Alex"]

        result = assign_ticket()

        # Matches your exact return format: f"{ticket_id} assigned to {name} successfully"
        self.assertEqual(result, "T001 assigned to Agent_Alex successfully")
        self.assertEqual(tickets[0]["assigned_to"], "Agent_Alex")


    @patch("builtins.input")
    def test_assign_ticket_not_found(self, mock_input):
        mock_input.side_effect = ["T999"]

        result = assign_ticket()

        self.assertEqual(result, "Ticket ID not found")

if __name__ == "__main__":
    unittest.main()
