# VITyarthi Library Management System

A modular Python + SQLite Library Management System built to meet the VITyarthi "Build Your Own Project" requirements.

## Major Functional Modules

1. Book Management
   - Add, list, search, update and delete books
   - Track total and available copies

2. Member Management
   - Add, list, update and delete library members
   - ACTIVE / INACTIVE member status

3. Issue / Return Management
   - Issue books
   - Return books
   - Automatic availability update
   - Automatic overdue fine calculation

4. Reports
   - Library dashboard
   - Active loan report
   - Loan history
   - Overdue report

## Technologies

- Python 3.10+
- SQLite3
- Object-oriented service classes
- Dataclasses
- Unit testing with unittest
- Git / GitHub for version control

## Project Structure

```text
Library_Management_System/
│
├── config.py
├── database.py
├── models.py
├── validators.py
├── book_service.py
├── member_service.py
├── issue_service.py
├── report_service.py
├── main.py
├── requirements.txt
├── README.md
├── statement.md
└── tests/
    └── test_library.py
```

## How to Run

1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Run:

```bash
python main.py
```

The `library.db` SQLite database is created automatically the first time the program starts.

## How to Test

Run:

```bash
python -m unittest discover -s tests -v
```

## Design Notes

- SQLite provides persistent storage without external database software.
- SQL queries use parameters instead of string concatenation.
- Services separate business logic from the CLI.
- Validation is kept in a separate module.
- Foreign keys protect relationships between books, members and loans.
- Books and members with loan history are protected from accidental deletion.

## Example Workflow

Add Book → Add Member → Issue Book → View Active Loans → Return Book → View Fine / Reports
