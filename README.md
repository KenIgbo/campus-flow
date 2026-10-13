# CampusFlow

CampusFlow is a command-line ticket management system designed to help IT departments manage and track support requests.

## Features

- Create support tickets
- Assign tickets to staff members
- Update ticket status
- View individual tickets
- List all tickets
- View prioritized work queue
- Generate ticket reports
- Save and load tickets using JSON storage

## Project Structure

```text
campusflow/
│
├── main.py
├── tickets.json
├── .gitignore
├── README.md
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   └── reports.py
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   └── test_storage.py
│ 
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md
```

## Requirements

- Python 3.12+
- unittest

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd campusflow
```

Create a virtual environment:

```bash
python -m venv env
```

Activate the environment:

Linux/macOS:

```bash
source env/bin/activate
```

Windows:

```bash
env\Scripts\activate
```

## Running the Application

```bash
python main.py
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Test Coverage

The test suite verifies:

- Ticket creation
- Ticket assignment
- Input validation
- Workflow transitions
- Status update rules
- Data persistence
- File loading and saving functionality

Current automated tests: 22