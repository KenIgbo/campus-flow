import unittest
from unittest.mock import patch
from campusflow.storage import tickets
from campusflow.workflow import update_status

class TestCampusFlowWorkflow(unittest.TestCase):

    def setUp(self):
        # Clear storage and seed a default ticket before every single test
        tickets.clear()
        tickets.append({
            "id": "T001",
            "title": "Network outage",
            "category": "network",
            "urgency": "high",
            "affected_users": 20,
            "priority": "critical",
            "status": "open",
            "assigned_to": "John"
        })

    # --- Workflow State Tests ---

    @patch("builtins.input")
    def test_update_status_success(self, mock_input):
        mock_input.side_effect = [
            "T001",
            "in_progress"
        ]

        result = update_status()

        self.assertEqual(result, "Status updated")
        self.assertEqual(tickets[0]["status"], "in_progress")

    @patch("builtins.input")
    def test_ticket_not_found(self, mock_input):
        mock_input.side_effect = [
            "T999"
        ]

        result = update_status()

        self.assertEqual(result, "Ticket ID not found")

    @patch("builtins.input")
    def test_open_to_in_progress(self, mock_input):
        tickets[0]["status"] = "open"
        mock_input.side_effect = [
            "T001",
            "in_progress"
        ]

        result = update_status()

        self.assertEqual(result, "Status updated")

    @patch("builtins.input")
    def test_open_to_resolved_rejected(self, mock_input):
        tickets[0]["status"] = "open"
        mock_input.side_effect = [
            "T001",
            "resolved"
        ]

        result = update_status()

        self.assertEqual(result, "Update rejected")

    @patch("builtins.input")
    def test_in_progress_to_open_rejected(self, mock_input):
        tickets[0]["status"] = "in_progress"
        mock_input.side_effect = [
            "T001",
            "open"
        ]

        result = update_status()

        self.assertEqual(result, "Update rejected")

    @patch("builtins.input")
    def test_in_progress_to_resolved(self, mock_input):
        tickets[0]["status"] = "in_progress"
        mock_input.side_effect = [
            "T001",
            "resolved"
        ]

        result = update_status()

        self.assertEqual(result, "Status updated")

    @patch("builtins.input")
    def test_update_unassigned_ticket(self, mock_input):
        tickets[0]["assigned_to"] = None
        mock_input.side_effect = [
            "T001",
            "in_progress"
        ]

        result = update_status()

        self.assertEqual(result, "Update rejected")

    @patch("builtins.input")
    def test_invalid_status(self, mock_input):
        mock_input.side_effect = [
            "T001",
            "closed"
        ]

        result = update_status()

        self.assertEqual(result, "Status not supported")

if __name__ == "__main__":
    unittest.main()
