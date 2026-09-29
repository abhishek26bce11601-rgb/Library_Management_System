from typing import Optional
from database import get_connection
from models import Member
from validators import clean_text, validate_email, validate_phone


class MemberService:
    def add_member(self, name: str, email: str, phone: str) -> int:
        name = clean_text(name, "Name")
        email = validate_email(email)
        phone = validate_phone(phone)

        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO members (name, email, phone)
                VALUES (?, ?, ?)
                """,
                (name, email, phone),
            )
            return cursor.lastrowid

    def list_members(self) -> list[Member]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM members ORDER BY name"
            ).fetchall()
        return [Member(**dict(row)) for row in rows]

    def get_member(self, member_id: int) -> Optional[Member]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM members WHERE id = ?", (member_id,)
            ).fetchone()
        return Member(**dict(row)) if row else None

    def update_member(
        self,
        member_id: int,
        name: str,
        email: str,
        phone: str,
        status: str,
    ) -> None:
        if not self.get_member(member_id):
            raise ValueError("Member not found.")

        name = clean_text(name, "Name")
        email = validate_email(email)
        phone = validate_phone(phone)
        status = status.strip().upper()

        if status not in {"ACTIVE", "INACTIVE"}:
            raise ValueError("Status must be ACTIVE or INACTIVE.")

        with get_connection() as conn:
            conn.execute(
                """
                UPDATE members
                SET name = ?, email = ?, phone = ?, status = ?
                WHERE id = ?
                """,
                (name, email, phone, status, member_id),
            )

    def delete_member(self, member_id: int) -> None:
        if not self.get_member(member_id):
            raise ValueError("Member not found.")

        with get_connection() as conn:
            loan = conn.execute(
                "SELECT 1 FROM loans WHERE member_id = ? LIMIT 1",
                (member_id,),
            ).fetchone()

            if loan:
                raise ValueError(
                    "This member has loan history and cannot be deleted."
                )

            conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
