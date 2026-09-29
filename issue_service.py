from datetime import date, timedelta
from database import get_connection
from config import DEFAULT_LOAN_DAYS, FINE_PER_DAY


class LoanService:
    def issue_book(
        self,
        book_id: int,
        member_id: int,
        loan_days: int = DEFAULT_LOAN_DAYS,
    ) -> int:
        if loan_days < 1:
            raise ValueError("Loan days must be at least 1.")

        today = date.today()
        due_date = today + timedelta(days=loan_days)

        with get_connection() as conn:
            book = conn.execute(
                "SELECT id, available_copies FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()
            if not book:
                raise ValueError("Book not found.")

            if book["available_copies"] <= 0:
                raise ValueError("No available copy of this book.")

            member = conn.execute(
                "SELECT id, status FROM members WHERE id = ?",
                (member_id,),
            ).fetchone()
            if not member:
                raise ValueError("Member not found.")

            if member["status"] != "ACTIVE":
                raise ValueError("Only ACTIVE members can borrow books.")

            duplicate = conn.execute(
                """
                SELECT 1 FROM loans
                WHERE book_id = ? AND member_id = ? AND status = 'ISSUED'
                LIMIT 1
                """,
                (book_id, member_id),
            ).fetchone()

            if duplicate:
                raise ValueError(
                    "This member already has an active loan for this book."
                )

            cursor = conn.execute(
                """
                INSERT INTO loans
                (book_id, member_id, issue_date, due_date, status)
                VALUES (?, ?, ?, ?, 'ISSUED')
                """,
                (book_id, member_id, today.isoformat(), due_date.isoformat()),
            )

            conn.execute(
                """
                UPDATE books
                SET available_copies = available_copies - 1
                WHERE id = ?
                """,
                (book_id,),
            )

            return cursor.lastrowid

    def return_book(self, loan_id: int) -> float:
        today = date.today()

        with get_connection() as conn:
            loan = conn.execute(
                """
                SELECT id, book_id, due_date, status
                FROM loans
                WHERE id = ?
                """,
                (loan_id,),
            ).fetchone()

            if not loan:
                raise ValueError("Loan record not found.")

            if loan["status"] == "RETURNED":
                raise ValueError("This book has already been returned.")

            due_date = date.fromisoformat(loan["due_date"])
            overdue_days = max((today - due_date).days, 0)
            fine = overdue_days * FINE_PER_DAY

            conn.execute(
                """
                UPDATE loans
                SET return_date = ?, fine = ?, status = 'RETURNED'
                WHERE id = ?
                """,
                (today.isoformat(), fine, loan_id),
            )

            conn.execute(
                """
                UPDATE books
                SET available_copies = available_copies + 1
                WHERE id = ?
                """,
                (loan["book_id"],),
            )

            return fine

    def list_active_loans(self):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT
                    l.id,
                    b.title AS book_title,
                    m.name AS member_name,
                    l.issue_date,
                    l.due_date,
                    l.status
                FROM loans l
                JOIN books b ON b.id = l.book_id
                JOIN members m ON m.id = l.member_id
                WHERE l.status = 'ISSUED'
                ORDER BY l.due_date
                """
            ).fetchall()

    def list_loan_history(self):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT
                    l.id,
                    b.title AS book_title,
                    m.name AS member_name,
                    l.issue_date,
                    l.due_date,
                    l.return_date,
                    l.fine,
                    l.status
                FROM loans l
                JOIN books b ON b.id = l.book_id
                JOIN members m ON m.id = l.member_id
                ORDER BY l.issue_date DESC, l.id DESC
                """
            ).fetchall()
