from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    id: Optional[int]
    isbn: str
    title: str
    author: str
    category: str
    total_copies: int
    available_copies: int
    created_at: Optional[str] = None


@dataclass
class Member:
    id: Optional[int]
    name: str
    email: str
    phone: str
    status: str = "ACTIVE"
    created_at: Optional[str] = None


@dataclass
class Loan:
    id: Optional[int]
    book_id: int
    member_id: int
    issue_date: str
    due_date: str
    return_date: Optional[str]
    fine: float
    status: str
