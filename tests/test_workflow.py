from unittest import TestCase
from unittest.mock import patch
from campusflow.storage import tickets
from campusflow.workflow import update_status, work_queue

class TestUpdateStatus(TestCase):

    def setUp(self):
        tickets.clear()

        self.ticket = {
            "id": "T001",
            "title": "Internet problem",
            "category": "network",
            "urgency": "high",
            "affected_users": 10,
            "priority": "critical",
            "status": "open",
            "assigned_to": "John",
            "notes": []
        }

        tickets.append(self.ticket)

        self.save_patcher = patch("campusflow.workflow.save_ticket")
        self.mock_save = self.save_patcher.start()

    def tearDown(self):
        self.save_patcher.stop()
        tickets.clear()

    def test_no_ticket_recorded(self):
        tickets.clear()

        result = update_status()

        self.assertEqual(result, "No ticket recorded")

    @patch("builtins.input", side_effect=[""])
    def test_empty_ticket_id(self, mock_input):
        result = update_status()

        self.assertEqual(result, "Ticket ID cannot be empty")

    @patch("builtins.input", side_effect=["T999"])
    def test_ticket_id_not_found(self, mock_input):
        result = update_status()

        self.assertEqual(result, "Ticket ID not found")

    @patch("builtins.input", side_effect=["T001", ""])
    def test_empty_status(self, mock_input):
        result = update_status()

        self.assertEqual(result, "Status cannot be empty")

    @patch("builtins.input", side_effect=["T001", "pending"])
    def test_unsupported_status(self, mock_input):
        result = update_status()

        self.assertEqual(result, "Status not supported")

    @patch("builtins.input", side_effect=["T001", "in_progress"])
    def test_update_open_to_in_progress(self, mock_input):
        result = update_status()

        self.assertEqual(result, "Status updated successfully")
        self.assertEqual(self.ticket["status"], "in_progress")
        self.mock_save.assert_called_once()

    @patch("builtins.input", side_effect=["T001", "open"])
    def test_status_already_open(self, mock_input):
        result = update_status()

        self.assertEqual(result, "Status already 'open'")
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "resolved"])
    def test_cannot_resolve_open_ticket(self, mock_input):
        result = update_status()

        self.assertEqual(
            result,
            "Cannot change status from 'open' to 'resolved'!"
        )
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "resolved"])
    def test_update_in_progress_to_resolved(self, mock_input):
        self.ticket["status"] = "in_progress"

        result = update_status()

        self.assertEqual(result, "Status updated successfully")
        self.assertEqual(self.ticket["status"], "resolved")
        self.mock_save.assert_called_once()

    @patch("builtins.input", side_effect=["T001", "open"])
    def test_cannot_change_in_progress_to_open(self, mock_input):
        self.ticket["status"] = "in_progress"

        result = update_status()

        self.assertEqual(
            result,
            "Cannot change status from 'in_progress' to 'open'!"
        )
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "in_progress"])
    def test_status_already_in_progress(self, mock_input):
        self.ticket["status"] = "in_progress"

        result = update_status()

        self.assertEqual(result, "Status already 'in_progress'")
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "resolved"])
    def test_status_already_resolved(self, mock_input):
        self.ticket["status"] = "resolved"

        result = update_status()

        self.assertEqual(result, "Status already 'resolved'")
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "in_progress"])
    def test_cannot_change_resolved_to_in_progress(self, mock_input):
        self.ticket["status"] = "resolved"

        result = update_status()

        self.assertEqual(
            result,
            "Cannot change status from 'resolved' to 'in_progress'!"
        )
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "open"])
    def test_cannot_update_unassigned_ticket(self, mock_input):
        self.ticket["assigned_to"] = None

        result = update_status()

        self.assertEqual(
            result,
            "Update rejected! ticket not assigned"
        )
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["T001", " IN_PROGRESS "])
    def test_status_is_trimmed_and_lowercased(self, mock_input):
        result = update_status()

        self.assertEqual(result, "Status updated successfully")
        self.assertEqual(self.ticket["status"], "in_progress")
        self.mock_save.assert_called_once()


class TestWorkQueue(TestCase):

    def setUp(self):
        tickets.clear()

        self.critical_ticket = {
            "id": "T001",
            "title": "Server failure",
            "category": "network",
            "urgency": "high",
            "affected_users": 20,
            "priority": "critical",
            "status": "open",
            "assigned_to": "John",
            "notes": []
        }

        self.high_ticket = {
            "id": "T002",
            "title": "WiFi problem",
            "category": "network",
            "urgency": "high",
            "affected_users": 5,
            "priority": "high",
            "status": "in_progress",
            "assigned_to": "Mary",
            "notes": []
        }

        self.medium_ticket = {
            "id": "T003",
            "title": "Software error",
            "category": "software",
            "urgency": "medium",
            "affected_users": 2,
            "priority": "medium",
            "status": "open",
            "assigned_to": "Peter",
            "notes": []
        }

        self.low_ticket = {
            "id": "T004",
            "title": "Mouse problem",
            "category": "hardware",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "open",
            "assigned_to": "Jane",
            "notes": []
        }

        self.resolved_ticket = {
            "id": "T005",
            "title": "Resolved network issue",
            "category": "network",
            "urgency": "high",
            "affected_users": 15,
            "priority": "critical",
            "status": "resolved",
            "assigned_to": "David",
            "notes": []
        }

    def tearDown(self):
        tickets.clear()

    def test_work_queue_with_no_tickets(self):
        with patch("builtins.print") as mock_print:
            work_queue()

        mock_print.assert_called_once_with("No ticket recorded")

    def test_work_queue_displays_heading(self):
        tickets.append(self.critical_ticket)

        with patch("builtins.print") as mock_print:
            work_queue()

        printed_output = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
        )

        self.assertIn("WORK QUEUE", printed_output)

    def test_work_queue_excludes_resolved_tickets(self):
        tickets.extend([
            self.critical_ticket,
            self.resolved_ticket
        ])

        with patch("builtins.print") as mock_print:
            work_queue()

        printed_output = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
        )

        self.assertIn("T001", printed_output)
        self.assertNotIn("T005", printed_output)

    def test_work_queue_orders_by_priority(self):
        # Insert the tickets in the wrong order deliberately.
        tickets.extend([
            self.low_ticket,
            self.medium_ticket,
            self.high_ticket,
            self.critical_ticket
        ])

        with patch("builtins.print") as mock_print:
            work_queue()

        printed_output = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
        )

        critical_position = printed_output.index("T001")
        high_position = printed_output.index("T002")
        medium_position = printed_output.index("T003")
        low_position = printed_output.index("T004")

        self.assertLess(critical_position, high_position)
        self.assertLess(high_position, medium_position)
        self.assertLess(medium_position, low_position)

    def test_work_queue_does_not_change_tickets(self):
        tickets.extend([
            self.critical_ticket,
            self.high_ticket,
            self.medium_ticket,
            self.low_ticket
        ])

        original_statuses = [
            ticket["status"] for ticket in tickets
        ]

        with patch("builtins.print"):
            work_queue()

        updated_statuses = [
            ticket["status"] for ticket in tickets
        ]

        self.assertEqual(original_statuses, updated_statuses)