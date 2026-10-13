# AI Learning Log

## Project: CampusFlow

## Overview

During the development of CampusFlow, AI was used as a learning and support tool to improve understanding of Python programming concepts, software design, testing, debugging, and project organization.

The final implementation and testing were completed after reviewing, understanding, and applying the suggestions provided.

---

## Learning Activity 1: Refactoring a Single File Project

### What I Learned

Initially, the entire application was contained in a single Python file. Through AI-assisted learning, I learned how to reorganize the code into multiple modules based on functionality.

### Modules Created

- tickets.py
- workflow.py
- storage.py
- reports.py
- main.py

### Benefit

This improved:

- Code organization
- Readability
- Maintainability
- Separation of concerns

---

## Learning Activity 2: Python Packages and Imports

### What I Learned

I learned how Python packages work and why an `__init__.py` file is required.

Examples of imports used:

```python
from campusflow.storage import tickets, save_ticket
from campusflow.workflow import update_status
```

### Benefit

This helped me understand how larger Python applications are structured across multiple files.

---

## Learning Activity 3: JSON Data Persistence

### What I Learned

I learned how to store and retrieve data using JSON files.

Examples:

```python
json.dump()
json.load()
```

I also learned how application data can persist between program executions without using a database.

### Benefit

This allowed ticket information to be saved and loaded automatically.

---

## Learning Activity 4: Debugging Global Variables

### What I Learned

While separating the program into modules, an issue occurred involving the global `tickets` list and JSON loading.

I learned how shared mutable objects behave when imported across modules and how this can affect program state.

### Benefit

This improved my understanding of Python namespaces, imports, and variable scope.

---

## Learning Activity 5: Automated Testing with Pytest

### What I Learned

I learned how to create automated tests using unittest.

Examples included testing:

- Ticket creation
- Ticket assignment
- Status updates
- Input validation
- Data storage 