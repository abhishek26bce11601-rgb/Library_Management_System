from typing import Optional
from database import get_connection
from models import Book
from validators import clean_text, validate_copies


class BookService:
    def add_book(
        self,
        isbn: str,
        title: str,
        author: str,
        category: str,
        copies: int,
    ) -> int:
        isbn = clean_text(isbn, "ISBN")
        title = clean_text(title, "Title")
        author = clean_text(author, "Author")
        category = clean_text(category, "Category")
        copies = validate_copies(copies)

        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO books
                (isbn, title, author, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (isbn, title, author, category, copies, copies),
            )
            return cursor.lastrowid

    def list_books(self) -> list[Book]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM books ORDER BY title"
            ).fetchall()
        return [Book(**dict(row)) for row in rows]

    def search_books(self, keyword: str) -> list[Book]:
        keyword = clean_text(keyword, "Search keyword")
        pattern = f"%{keyword}%"
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM books
                WHERE isbn LIKE ?
                   OR title LIKE ?
                   OR author LIKE ?
                   OR category LIKE ?
                ORDER BY title
                """,
                (pattern, pattern, pattern, pattern),
            ).fetchall()
        return [Book(**dict(row)) for row in rows]

    def get_book(self, book_id: int) -> Optional[Book]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM books WHERE id = ?", (book_id,)
            ).fetchone()
        return Book(**dict(row)) if row else None

    def update_book(
        self,
        book_id: int,
        title: str,
        author: str,
        category: str,
        total_copies: int,
    ) -> None:
        book = self.get_book(book_id)
        if not book:
            raise ValueError("Book not found.")

        title = clean_text(title, "Title")
        author = clean_text(author, "Author")
        category = clean_text(category, "Category")
        total_copies = validate_copies(total_copies)

        issued_copies = book.total_copies - book.available_copies
        if total_copies < issued_copies:
            raise ValueError(
                f"Total copies cannot be less than currently issued copies ({issued_copies})."
            )

        available_copies = total_copies - issued_copies

        with get_connection() as conn:
            conn.execute(
                """
                UPDATE books
                SET title = ?, author = ?, category = ?,
                    total_copies = ?, available_copies = ?
                WHERE id = ?
                """,
                (
                    title,
                    author,
                    category,
                    total_copies,
                    available_copies,
                    book_id,
                ),
            )

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        if not book:
            raise ValueError("Book not found.")

        with get_connection() as conn:
            loan = conn.execute(
                "SELECT 1 FROM loans WHERE book_id = ? LIMIT 1", (book_id,)
            ).fetchone()

            if loan:
                raise ValueError(
                    "This book has loan history and cannot be deleted."
                )

            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
