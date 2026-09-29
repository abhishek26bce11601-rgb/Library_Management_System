from database import initialize_database
from book_service import BookService
from member_service import MemberService
from issue_service import LoanService
from report_service import ReportService


book_service = BookService()
member_service = MemberService()
loan_service = LoanService()
report_service = ReportService()


def read_int(prompt: str, minimum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            if minimum is None:
                print("Enter a valid integer.")
            else:
                print(f"Enter an integer >= {minimum}.")


def print_books(books) -> None:
    if not books:
        print("\nNo books found.")
        return

    print("\nID | ISBN | Title | Author | Category | Copies | Available")
    print("-" * 100)
    for book in books:
        print(
            f"{book.id} | {book.isbn} | {book.title} | {book.author} | "
            f"{book.category} | {book.total_copies} | {book.available_copies}"
        )


def print_members(members) -> None:
    if not members:
        print("\nNo members found.")
        return

    print("\nID | Name | Email | Phone | Status")
    print("-" * 75)
    for member in members:
        print(
            f"{member.id} | {member.name} | {member.email} | "
            f"{member.phone} | {member.status}"
        )


def add_book():
    try:
        isbn = input("ISBN: ")
        title = input("Title: ")
        author = input("Author: ")
        category = input("Category: ")
        copies = read_int("Number of copies: ", 1)

        book_id = book_service.add_book(
            isbn, title, author, category, copies
        )
        print(f"Book added successfully. Book ID: {book_id}")
    except Exception as exc:
        print(f"Error: {exc}")


def search_books():
    try:
        keyword = input("Search by ISBN/title/author/category: ")
        print_books(book_service.search_books(keyword))
    except Exception as exc:
        print(f"Error: {exc}")


def update_book():
    try:
        book_id = read_int("Book ID: ", 1)
        book = book_service.get_book(book_id)
        if not book:
            print("Book not found.")
            return

        title = input(f"Title [{book.title}]: ").strip() or book.title
        author = input(f"Author [{book.author}]: ").strip() or book.author
        category = (
            input(f"Category [{book.category}]: ").strip() or book.category
        )

        copies_input = input(
            f"Total copies [{book.total_copies}]: "
        ).strip()
        copies = int(copies_input) if copies_input else book.total_copies

        book_service.update_book(
            book_id, title, author, category, copies
        )
        print("Book updated successfully.")
    except Exception as exc:
        print(f"Error: {exc}")


def delete_book():
    try:
        book_id = read_int("Book ID: ", 1)
        book_service.delete_book(book_id)
        print("Book deleted successfully.")
    except Exception as exc:
        print(f"Error: {exc}")


def add_member():
    try:
        name = input("Name: ")
        email = input("Email: ")
        phone = input("10-digit phone: ")

        member_id = member_service.add_member(name, email, phone)
        print(f"Member added successfully. Member ID: {member_id}")
    except Exception as exc:
        print(f"Error: {exc}")


def update_member():
    try:
        member_id = read_int("Member ID: ", 1)
        member = member_service.get_member(member_id)
        if not member:
            print("Member not found.")
            return

        name = input(f"Name [{member.name}]: ").strip() or member.name
        email = input(f"Email [{member.email}]: ").strip() or member.email
        phone = input(f"Phone [{member.phone}]: ").strip() or member.phone
        status = (
            input(f"Status ACTIVE/INACTIVE [{member.status}]: ").strip().upper()
            or member.status
        )

        member_service.update_member(
            member_id, name, email, phone, status
        )
        print("Member updated successfully.")
    except Exception as exc:
        print(f"Error: {exc}")


def delete_member():
    try:
        member_id = read_int("Member ID: ", 1)
        member_service.delete_member(member_id)
        print("Member deleted successfully.")
    except Exception as exc:
        print(f"Error: {exc}")


def issue_book():
    try:
        book_id = read_int("Book ID: ", 1)
        member_id = read_int("Member ID: ", 1)

        custom_days = input(
            "Loan period in days [14]: "
        ).strip()
        loan_days = int(custom_days) if custom_days else 14

        loan_id = loan_service.issue_book(
            book_id, member_id, loan_days
        )
        print(f"Book issued successfully. Loan ID: {loan_id}")
    except Exception as exc:
        print(f"Error: {exc}")


def return_book():
    try:
        loan_id = read_int("Loan ID: ", 1)
        fine = loan_service.return_book(loan_id)
        print(f"Book returned successfully. Fine: ₹{fine:.2f}")
    except Exception as exc:
        print(f"Error: {exc}")


def show_active_loans():
    rows = loan_service.list_active_loans()
    if not rows:
        print("\nNo active loans.")
        return

    print("\nLoan ID | Book | Member | Issue Date | Due Date | Status")
    print("-" * 100)
    for row in rows:
        print(
            f"{row['id']} | {row['book_title']} | {row['member_name']} | "
            f"{row['issue_date']} | {row['due_date']} | {row['status']}"
        )


def show_loan_history():
    rows = loan_service.list_loan_history()
    if not rows:
        print("\nNo loan history.")
        return

    print(
        "\nLoan ID | Book | Member | Issue Date | Due Date | Return Date | "
        "Fine | Status"
    )
    print("-" * 125)
    for row in rows:
        print(
            f"{row['id']} | {row['book_title']} | {row['member_name']} | "
            f"{row['issue_date']} | {row['due_date']} | "
            f"{row['return_date'] or '-'} | ₹{row['fine']:.2f} | {row['status']}"
        )


def show_dashboard():
    data = report_service.dashboard()
    print("\n========== LIBRARY DASHBOARD ==========")
    print(f"Unique titles        : {data['unique_titles']}")
    print(f"Total copies         : {data['total_copies']}")
    print(f"Available copies     : {data['available_copies']}")
    print(f"Active members       : {data['active_members']}")
    print(f"Currently issued     : {data['currently_issued']}")
    print(f"Overdue loans        : {data['overdue_loans']}")
    print(f"Total fines          : ₹{data['total_fines_collected']:.2f}")


def show_overdue_report():
    rows = report_service.overdue_report()
    if not rows:
        print("\nNo overdue loans.")
        return

    print("\nLoan ID | Book | Member | Phone | Due Date | Overdue Days")
    print("-" * 100)
    for row in rows:
        print(
            f"{row['loan_id']} | {row['book_title']} | {row['member_name']} | "
            f"{row['phone']} | {row['due_date']} | {row['overdue_days']}"
        )


def books_menu():
    while True:
        print(
            """
--- BOOK MANAGEMENT ---
1. Add book
2. List books
3. Search books
4. Update book
5. Delete book
0. Back
"""
        )
        choice = input("Choose: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            print_books(book_service.list_books())
        elif choice == "3":
            search_books()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def members_menu():
    while True:
        print(
            """
--- MEMBER MANAGEMENT ---
1. Add member
2. List members
3. Update member
4. Delete member
0. Back
"""
        )
        choice = input("Choose: ").strip()

        if choice == "1":
            add_member()
        elif choice == "2":
            print_members(member_service.list_members())
        elif choice == "3":
            update_member()
        elif choice == "4":
            delete_member()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def loan_menu():
    while True:
        print(
            """
--- ISSUE / RETURN MANAGEMENT ---
1. Issue book
2. Return book
3. Active loans
4. Loan history
0. Back
"""
        )
        choice = input("Choose: ").strip()

        if choice == "1":
            issue_book()
        elif choice == "2":
            return_book()
        elif choice == "3":
            show_active_loans()
        elif choice == "4":
            show_loan_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def report_menu():
    while True:
        print(
            """
--- REPORTS ---
1. Dashboard
2. Overdue report
0. Back
"""
        )
        choice = input("Choose: ").strip()

        if choice == "1":
            show_dashboard()
        elif choice == "2":
            show_overdue_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def main():
    initialize_database()

    while True:
        print(
            f"""
==============================================
      VITyarthi Library Management System
==============================================
1. Book Management
2. Member Management
3. Issue / Return
4. Reports
0. Exit
"""
        )

        choice = input("Choose an option: ").strip()

        if choice == "1":
            books_menu()
        elif choice == "2":
            members_menu()
        elif choice == "3":
            loan_menu()
        elif choice == "4":
            report_menu()
        elif choice == "0":
            print("Thank you. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
