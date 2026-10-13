# Design Decisions

## Project Overview

CampusFlow is a command-line ticket management system designed to help a campus IT department manage support requests. The system allows users to create tickets, assign them to staff members, update ticket statuses, generate reports, and maintain a prioritized work queue.

---

## Decision 1: Modular System Design

### Decision

The original implementation was developed as a single Python file. The application was later reorganized into multiple modules:

- tickets.py
- workflow.py
- storage.py
- reports.py
- main.py

### Reason

Separating the application into modules improves:

- Readability
- Maintainability
- Reusability
- Testing

Each module is responsible for a specific part of the system.

---

## Decision 2: Function-Based Design

### Decision

The project uses functions instead of classes and objects.

### Reason

The system requirements can be effectively implemented using procedural programming techniques. A function-based approach keeps the solution simple while still meeting all functional requirements.

Examples include:

- create_ticket()
- assign_ticket()
- update_status()
- view_reports()

---

## Decision 3: JSON File Storage

### Decision

Ticket data is stored in a JSON file named:

```text
tickets.json
```

### Reason

JSON storage was chosen because:

- It is lightweight.
- It is easy to read and edit.
- No database installation is required.
- Python provides built-in support through the json module.

This allows ticket data to persist even after the application is closed.

---

## Decision 4: Automatic Priority Calculation

### Decision

Ticket priority is calculated automatically using:

- Urgency level
- Number of affected users

### Reason

Automatically calculating priority ensures consistency and removes subjectivity from the ticket management process.

The priority levels are:

- Critical
- High
- Medium
- Low

This helps ensure that more severe incidents are addressed first.

---

## Decision 5: Workflow Validation Rules

### Decision

The system enforces restrictions on status updates.

Allowed transitions include:

- Open → In Progress
- In Progress → Resolved

Rejected transitions include:

- Open → Resolved
- In Progress → Open

### Reason

These rules reflect a realistic ticket-handling process and prevent invalid workflow transitions.

A ticket must also be assigned before its status can be updated.

---

## Decision 6: Input Validation

### Decision

The application validates user inputs before processing data.

Validation includes:

- Empty title checks
- Empty category checks
- Supported category validation
- Supported urgency validation
- Numeric affected-user validation
- Positive affected-user validation

### Reason

Validation improves data quality and prevents invalid records from being stored.

---

## Decision 7: Unique Ticket Identification

### Decision

Each new ticket receives a unique identifier.

Examples:

```text
T001
T002
T003
```

### Reason

Unique identifiers make it easy to locate, view, assign, and update specific tickets.

---

## Decision 8: Automated Testing

### Decision

Automated tests were created using Pytest.

### Reason

Automated testing helps verify that system functionality continues to work correctly after code changes.

The test suite covers:

- Ticket creation
- Ticket assignment
- Input validation
- Status updates
- Workflow restrictions
- Data persistence
- File loading and saving

### Test Results

The final test suite contains 20 tests.

Example command:

```bash
python -m unittest discover -s tests -v
```

Result:

```text
22 passed
```

---

## Conclusion

The final design focuses on simplicity, reliability, maintainability, and correctness. The modular structure, automated testing, validation rules, and JSON-based persistence provide a robust solution for managing campus IT support tickets while meeting the project requirements.