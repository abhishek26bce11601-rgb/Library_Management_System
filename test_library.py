import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import database
from book_service import BookService
from member_service import MemberService
from issue_service import LoanService


class LibrarySystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()

        self.original_db = database.DB_FILE
        database.DB_FILE = Path(self.temp_db.name)
        database.initialize_database()

        self.books = BookService()
        self.members = MemberService()
        self.loans = LoanService()

    def tearDown(self):
        database.DB_FILE = self.original_db
        Path(self.temp_db.name).unlink(missing_ok=True)

    def test_add_book(self):
        book_id = self.books.add_book(
            "978000000001",
            "Python Basics",
            "John Doe",
            "Programming",
            3,
        )
        book = self.books.get_book(book_id)

        self.assertIsNotNone(book)
        self.assertEqual(book.available_copies, 3)

    def test_issue_and_return_book_with_fine(self):
        book_id = self.books.add_book(
            "978000000002",
            "SQL Guide",
            "Jane Doe",
            "Database",
            1,
        )
        member_id = self.members.add_member(
            "Amartya",
            "student@example.com",
            "9876543210",
        )

        loan_id = self.loans.issue_book(book_id, member_id, 14)

        # Make the loan overdue without mocking datetime.
        with database.get_connection() as conn:
            overdue_date = date.today() - timedelta(days=5)
            conn.execute(
                "UPDATE loans SET due_date = ? WHERE id = ?",
                (overdue_date.isoformat(), loan_id),
            )

        fine = self.loans.return_book(loan_id)

        book = self.books.get_book(book_id)
        self.assertEqual(book.available_copies, 1)
        self.assertEqual(fine, 25.0)

    def test_inactive_member_cannot_borrow(self):
        book_id = self.books.add_book(
            "978000000003",
            "Networks",
            "Author",
            "Computer Science",
            1,
        )
        member_id = self.members.add_member(
            "Inactive User",
            "inactive@example.com",
            "9123456789",
        )
        self.members.update_member(
            member_id,
            "Inactive User",
            "inactive@example.com",
            "9123456789",
            "INACTIVE",
        )

        with self.assertRaises(ValueError):
            self.loans.issue_book(book_id, member_id)

    def test_duplicate_active_loan_is_blocked(self):
        book_id = self.books.add_book(
            "978000000004",
            "Data Structures",
            "Author",
            "DSA",
            2,
        )
        member_id = self.members.add_member(
            "User",
            "user@example.com",
            "9012345678",
        )

        self.loans.issue_book(book_id, member_id)

        with self.assertRaises(ValueError):
            self.loans.issue_book(book_id, member_id)


if __name__ == "__main__":
    unittest.main()
