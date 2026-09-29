from datetime import date
from database import get_connection


class ReportService:
    def dashboard(self) -> dict:
        with get_connection() as conn:
            books = conn.execute(
                "SELECT COUNT(*) AS count, COALESCE(SUM(total_copies), 0) AS copies FROM books"
            ).fetchone()

            available = conn.execute(
                "SELECT COALESCE(SUM(available_copies), 0) AS copies FROM books"
            ).fetchone()

            members = conn.execute(
                "SELECT COUNT(*) AS count FROM members WHERE status = 'ACTIVE'"
            ).fetchone()

            issued = conn.execute(
                "SELECT COUNT(*) AS count FROM loans WHERE status = 'ISSUED'"
            ).fetchone()

            overdue = conn.execute(
                """
                SELECT COUNT(*) AS count
                FROM loans
                WHERE status = 'ISSUED' AND due_date < ?
                """,
                (date.today().isoformat(),),
            ).fetchone()

            fines = conn.execute(
                "SELECT COALESCE(SUM(fine), 0) AS total FROM loans"
            ).fetchone()

        return {
            "unique_titles": books["count"],
            "total_copies": books["copies"],
            "available_copies": available["copies"],
            "active_members": members["count"],
            "currently_issued": issued["count"],
            "overdue_loans": overdue["count"],
            "total_fines_collected": float(fines["total"]),
        }

    def overdue_report(self):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT
                    l.id AS loan_id,
                    b.title AS book_title,
                    m.name AS member_name,
                    m.phone,
                    l.issue_date,
                    l.due_date,
                    CAST(julianday('now') - julianday(l.due_date) AS INTEGER) AS overdue_days
                FROM loans l
                JOIN books b ON b.id = l.book_id
                JOIN members m ON m.id = l.member_id
                WHERE l.status = 'ISSUED'
                  AND l.due_date < ?
                ORDER BY l.due_date
                """,
                (date.today().isoformat(),),
            ).fetchall()
