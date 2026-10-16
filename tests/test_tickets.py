import unittest
from unittest.mock import patch
from campusflow import tickets as ticket_module
from campusflow.storage import tickets


class TestCampusFlowTickets(unittest.TestCase):

    def setUp(self):
        # Start with an empty ticket list before every test.
        tickets.clear()

        # Prevent save_ticket() from writing to tickets.json.
        self.save_patcher = patch("campusflow.tickets.save_ticket")
        self.mock_save_ticket = self.save_patcher.start()

    def tearDown(self):
        # Restore save_ticket() after each test.
        self.save_patcher.stop()

        # Clean up the shared ticket list.
        tickets.clear()

    def make_ticket(
        self,
        ticket_id="T001",
        title="Network issue",
        category="network",
        urgency="high",
        affected_users=10,
        priority="critical",
        status="open",
        assigned_to="Samuel",
        notes=None
    ):
        """Create a sample ticket without writing to disk."""
        ticket = {
            "id": ticket_id,
            "title": title,
            "category": category,
            "urgency": urgency,
            "affected_users": affected_users,
            "priority": priority,
            "status": status,
            "assigned_to": assigned_to,
            "notes": [] if notes is None else notes
        }

        tickets.append(ticket)
        return ticket

    # --------------------------------------------------
    # TEST gen_id()
    # --------------------------------------------------

    def test_gen_id_when_no_tickets_exist(self):
        self.assertEqual(ticket_module.gen_id(), "T001")

    def test_gen_id_when_ticket_exists(self):
        self.make_ticket(ticket_id="T001")

        self.assertEqual(ticket_module.gen_id(), "T002")

    def test_gen_id_with_multiple_tickets(self):
        self.make_ticket(ticket_id="T001")
        self.make_ticket(ticket_id="T002")

        self.assertEqual(ticket_module.gen_id(), "T003")

    # --------------------------------------------------
    # TEST note_id()
    # --------------------------------------------------

    def test_note_id_when_no_notes_exist(self):
        ticket = self.make_ticket()

        ticket_module.target_ticket = ticket

        self.assertEqual(ticket_module.note_id(), "N001")

    def test_note_id_when_notes_exist(self):
        ticket = self.make_ticket(
            notes=[
                {
                    "note_id": "N001",
                    "author": "Samuel",
                    "message": "Checking the router"
                }
            ]
        )

        ticket_module.target_ticket = ticket

        self.assertEqual(ticket_module.note_id(), "N002")

    # --------------------------------------------------
    # TEST cal_priority()
    # --------------------------------------------------

    def test_cal_priority_critical(self):
        ticket_module.urgency = "high"
        ticket_module.affected_users_val = 10

        self.assertEqual(ticket_module.cal_priority(), "critical")

    def test_cal_priority_high_due_to_urgency(self):
        ticket_module.urgency = "high"
        ticket_module.affected_users_val = 2

        self.assertEqual(ticket_module.cal_priority(), "high")

    def test_cal_priority_high_due_to_affected_users(self):
        ticket_module.urgency = "low"
        ticket_module.affected_users_val = 10

        self.assertEqual(ticket_module.cal_priority(), "high")

    def test_cal_priority_medium_due_to_urgency(self):
        ticket_module.urgency = "medium"
        ticket_module.affected_users_val = 1

        self.assertEqual(ticket_module.cal_priority(), "medium")

    def test_cal_priority_medium_due_to_affected_users(self):
        ticket_module.urgency = "low"
        ticket_module.affected_users_val = 3

        self.assertEqual(ticket_module.cal_priority(), "medium")

    def test_cal_priority_low(self):
        ticket_module.urgency = "low"
        ticket_module.affected_users_val = 2

        self.assertEqual(ticket_module.cal_priority(), "low")

    # --------------------------------------------------
    # TEST create_ticket()
    # --------------------------------------------------

    @patch("builtins.input", side_effect=[
        "network problem", "network", "high", "10"
    ])
    def test_create_ticket_successfully(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Ticket created successfully\n")
        self.assertEqual(len(tickets), 1)

        ticket = tickets[0]

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Network problem")
        self.assertEqual(ticket["category"], "network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 10)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(ticket["notes"], [])

        self.mock_save_ticket.assert_called_once()

    @patch("builtins.input", side_effect=["   "])
    def test_create_ticket_empty_title(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Title cannot be empty")
        self.assertEqual(tickets, [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=["Network issue", ""])
    def test_create_ticket_empty_category(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Category cannot be empty")
        self.assertEqual(tickets, [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=["Network issue", "invalid"])
    def test_create_ticket_unsupported_category(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Category not supported")
        self.assertEqual(tickets, [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "Network issue", "network", ""
    ])
    def test_create_ticket_empty_urgency(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Urgency cannot be empty")
        self.assertEqual(tickets, [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "Network issue", "network", "urgent"
    ])
    def test_create_ticket_unsupported_urgency(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Urgency not supported")
        self.assertEqual(tickets, [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "Network issue", "network", "low", "abc"
    ])
    def test_create_ticket_non_integer_affected_users(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Input must be a whole number")
        self.assertEqual(tickets, [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "Network issue", "network", "low", "0"
    ])
    def test_create_ticket_affected_users_must_be_positive(self, mock_input):
        result = ticket_module.create_ticket()

        self.assertEqual(result, "Input must be greater than zero")
        self.assertEqual(tickets, [])
        self.mock_save_ticket.assert_not_called()

    # --------------------------------------------------
    # TEST assign_ticket()
    # --------------------------------------------------

    def test_assign_ticket_when_no_tickets_exist(self):
        result = ticket_module.assign_ticket()

        self.assertEqual(result, "No ticket recorded")
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "Jerome"])
    def test_assign_ticket_successfully(self, mock_input):
        self.make_ticket(assigned_to=None)

        result = ticket_module.assign_ticket()

        self.assertEqual(
            result,
            "T001 assigned to Jerome successfully"
        )
        self.assertEqual(tickets[0]["assigned_to"], "Jerome")
        self.mock_save_ticket.assert_called_once()

    @patch("builtins.input", return_value="   ")
    def test_assign_ticket_empty_id(self, mock_input):
        self.make_ticket()

        result = ticket_module.assign_ticket()

        self.assertEqual(result, "Ticket ID cannot be empty")
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", return_value="T999")
    def test_assign_ticket_unknown_id(self, mock_input):
        self.make_ticket()

        result = ticket_module.assign_ticket()

        self.assertEqual(result, "Ticket ID not found")
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=["T001", "   "])
    def test_assign_ticket_empty_staff_name(self, mock_input):
        self.make_ticket(assigned_to=None)

        result = ticket_module.assign_ticket()

        self.assertEqual(result, "Name cannot be empty")
        self.assertIsNone(tickets[0]["assigned_to"])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", return_value="T001")
    def test_assign_ticket_resolved_ticket(self, mock_input):
        self.make_ticket(status="resolved")

        result = ticket_module.assign_ticket()

        self.assertEqual(
            result,
            "Cannot reassign a resolved ticket"
        )
        self.mock_save_ticket.assert_not_called()

    # --------------------------------------------------
    # TEST list_tickets()
    # --------------------------------------------------

    def test_list_tickets_when_empty(self):
        with patch("builtins.print") as mock_print:
            result = ticket_module.list_tickets()

        mock_print.assert_called_once_with("No ticket recorded")
        self.assertIsNone(result)

    def test_list_tickets_displays_ticket_information(self):
        self.make_ticket()

        with patch("builtins.print") as mock_print:
            ticket_module.list_tickets()

        printed_text = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
        )

        self.assertIn("T001", printed_text)
        self.assertIn("Network issue", printed_text)
        self.assertIn("CATEGORY", printed_text)
        self.assertIn("PRIORITY", printed_text)
        self.assertIn("Samuel", printed_text)

    # --------------------------------------------------
    # TEST view_ticket()
    # --------------------------------------------------

    def test_view_ticket_when_empty(self):
        result = ticket_module.view_ticket()

        self.assertEqual(result, "No ticket recorded")

    @patch("builtins.input", return_value="   ")
    def test_view_ticket_empty_id(self, mock_input):
        self.make_ticket()

        result = ticket_module.view_ticket()

        self.assertEqual(result, "Ticket ID cannot be empty")

    @patch("builtins.input", return_value="T999")
    def test_view_ticket_unknown_id(self, mock_input):
        self.make_ticket()

        result = ticket_module.view_ticket()

        self.assertEqual(result, "ID not found")

    @patch("builtins.input", return_value="T001")
    def test_view_ticket_successfully(self, mock_input):
        self.make_ticket()

        result = ticket_module.view_ticket()

        self.assertIn("DETAILS OF T001", result)
        self.assertIn("Network issue", result)
        self.assertIn("Assigned_to", result)
        self.assertIn("Notes", result)

    # --------------------------------------------------
    # TEST add_note()
    # --------------------------------------------------

    def test_add_note_when_no_tickets_exist(self):
        result = ticket_module.add_note()

        self.assertEqual(result, "No ticket recorded")
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", return_value="   ")
    def test_add_note_empty_ticket_id(self, mock_input):
        self.make_ticket()

        result = ticket_module.add_note()

        self.assertEqual(result, "Ticket ID cannot be empty")
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", return_value="T999")
    def test_add_note_unknown_ticket_id(self, mock_input):
        self.make_ticket()

        result = ticket_module.add_note()

        self.assertEqual(result, "ID not found")
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "T001"
    ])
    def test_add_note_ticket_not_assigned(self, mock_input):
        self.make_ticket(assigned_to=None)

        result = ticket_module.add_note()

        self.assertEqual(
            result,
            "Update rejected! ticket not assigned"
        )
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "T001"
    ])
    def test_add_note_to_resolved_ticket(self, mock_input):
        self.make_ticket(status="resolved")

        result = ticket_module.add_note()

        self.assertEqual(
            result,
            "A resolved ticket cannot accept a new note"
        )
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "T001", "   "
    ])
    def test_add_note_empty_author(self, mock_input):
        self.make_ticket()

        result = ticket_module.add_note()

        self.assertEqual(result, "Author name cannot be empty")
        self.assertEqual(tickets[0]["notes"], [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "T001", "Samuel", "   "
    ])
    def test_add_note_empty_message(self, mock_input):
        self.make_ticket()

        result = ticket_module.add_note()

        self.assertEqual(result, "Message cannot be empty")
        self.assertEqual(tickets[0]["notes"], [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "T001", "Samuel", "Bad"
    ])
    def test_add_note_message_too_short(self, mock_input):
        self.make_ticket()

        result = ticket_module.add_note()

        self.assertEqual(
            result,
            "Message must contain 5-300 characters"
        )
        self.assertEqual(tickets[0]["notes"], [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "T001", "Samuel", "A" * 301
    ])
    def test_add_note_message_too_long(self, mock_input):
        self.make_ticket()

        result = ticket_module.add_note()

        self.assertEqual(
            result,
            "Message must contain 5-300 characters"
        )
        self.assertEqual(tickets[0]["notes"], [])
        self.mock_save_ticket.assert_not_called()

    @patch("builtins.input", side_effect=[
        "T001", "  Samuel  ", "  Checking router  "
    ])
    def test_add_note_successfully(self, mock_input):
        self.make_ticket()

        result = ticket_module.add_note()

        self.assertEqual(result, "Note added sucessfully")
        self.assertEqual(
            tickets[0]["notes"],
            [
                {
                    "note_id": "N001",
                    "author": "Samuel",
                    "message": "Checking router"
                }
            ]
        )
        self.mock_save_ticket.assert_called_once()

    @patch("builtins.input", side_effect=[
        "T001", "Jerome", "Checking network cable"
    ])
    def test_add_second_note_gets_next_id(self, mock_input):
        self.make_ticket(
            notes=[
                {
                    "note_id": "N001",
                    "author": "Samuel",
                    "message": "Checking router"
                }
            ]
        )

        result = ticket_module.add_note()

        self.assertEqual(result, "Note added sucessfully")
        self.assertEqual(
            tickets[0]["notes"][-1]["note_id"],
            "N002"
        )

    # --------------------------------------------------
    # TEST view_ticket_notes()
    # --------------------------------------------------

    def test_view_ticket_notes_when_no_tickets_exist(self):
        with patch("builtins.print") as mock_print:
            result = ticket_module.view_ticket_notes()

        mock_print.assert_called_once_with("No ticket recorded")
        self.assertIsNone(result)

    @patch("builtins.input", return_value="   ")
    def test_view_ticket_notes_empty_id(self, mock_input):
        self.make_ticket()

        with patch("builtins.print") as mock_print:
            result = ticket_module.view_ticket_notes()

        mock_print.assert_called_once_with(
            "Ticket ID cannot be empty"
        )
        self.assertIsNone(result)

    @patch("builtins.input", return_value="T999")
    def test_view_ticket_notes_unknown_id(self, mock_input):
        self.make_ticket()

        with patch("builtins.print") as mock_print:
            ticket_module.view_ticket_notes()

        mock_print.assert_called_once_with("ID not found")

    @patch("builtins.input", return_value="T001")
    def test_view_ticket_notes_when_no_notes_exist(self, mock_input):
        self.make_ticket()

        with patch("builtins.print") as mock_print:
            ticket_module.view_ticket_notes()

        mock_print.assert_called_once_with("No notes for this Ticket")

    @patch("builtins.input", return_value="T001")
    def test_view_ticket_notes_displays_notes(self, mock_input):
        self.make_ticket(
            notes=[
                {
                    "note_id": "N001",
                    "author": "Samuel",
                    "message": "Checking router"
                }
            ]
        )

        with patch("builtins.print") as mock_print:
            ticket_module.view_ticket_notes()

        printed_text = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
        )

        self.assertIn("N001", printed_text)
        self.assertIn("Samuel", printed_text)
        self.assertIn("Checking router", printed_text)

    # --------------------------------------------------
    # VERIFY THAT TESTS DO NOT WRITE TO DISK
    # --------------------------------------------------

    def test_save_ticket_is_mocked(self):
        self.make_ticket()

        # This function should not write to disk.
        with patch("builtins.input", side_effect=[
            "T001", "Jerome"
        ]):
            ticket_module.assign_ticket()

        self.mock_save_ticket.assert_called_once()


if __name__ == "__main__":
    unittest.main()