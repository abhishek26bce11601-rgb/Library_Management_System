# Library Management System — Project Statement and Scope

---

## 1. Problem Statement

Traditional and legacy library workflows rely heavily on manual record-keeping, spreadsheets, or fragmented desktop applications. These outdated approaches introduce significant operational bottlenecks, including:

* **Inefficient Circulation Workflows:** Manual check-ins and check-outs lead to long queues, human error in recording due dates, and misplaced physical logs.
* **Lack of Real-Time Visibility:** Patrons cannot easily check book availability, hold status, or due dates remotely, leading to unnecessary library visits and friction.
* **Manual Fine & Due Date Tracking:** Librarians spend substantial time manually identifying overdue materials, calculating late fees, and contacting borrowers.
* **Inventory Mismanagement:** Without automated tracking, lost, damaged, or misplaced books are difficult to reconcile, resulting in inaccurate catalog data.
* **Poor Analytics & Reporting:** Library administrators lack real-time data on catalog utilization, borrowing trends, active user metrics, and inventory health to make informed procurement decisions.

To address these challenges, a centralized, modern **Library Management System (LMS)** is required to streamline operations, enhance user experience for patrons, and provide actionable analytics for management.

---

## 2. Scope of the Project

### 2.1 In-Scope
* **User & Role Management:** Secure authentication and Role-Based Access Control (RBAC) for Admins, Librarians, and Members.
* **Catalog & Inventory Management:** Full CRUD (Create, Read, Update, Delete) operations for books, media, categories, authors, and ISBN-based inventory tracking.
* **Circulation Management:** Automated checkout, check-in, renewal workflows, loan period enforcement, and maximum borrowing limits.
* **Reservation & Hold System:** Ability for members to reserve currently borrowed books, with automated queue management when items are returned.
* **Automated Fine & Notification Management:** Automatic calculation of late fees based on configured daily rates, alongside automated notification alerts for upcoming due dates and overdue items.
* **Search & Discovery Engine:** Real-time catalog search with filtering by title, author, genre, ISBN, and stock availability.
* **Analytics & Reporting Dashboard:** Visual reporting on popular titles, overdue logs, revenue from fines, user activity, and circulation statistics.

### 2.2 Out-of-Scope (Future Enhancements)
* Physical hardware integration for RFID/gate security scanners (software interfaces provided, but physical hardware installation is excluded).
* Digital Rights Management (DRM) media server or built-in PDF/E-pub reader engines.
* Inter-library loaning systems across external, multi-institutional library networks.
* Third-party payment gateway merchant setup (mock/simulated payment interfaces included).

---

## 3. Target Users

| User Role | Description & Responsibilities | Key Needs |
| :--- | :--- | :--- |
| **System Administrator** | Technical manager responsible for platform health, role provisioning, and system configuration. | Role management, security logging, global configuration, database backup settings. |
| **Librarian / Staff** | Operational user handling desk management, cataloging, and inventory maintenance. | Rapid checkout/check-in interface, fine collection, inventory updates, reserve queue processing. |
| **Library Member / Reader** | End-users (students, faculty, or public patrons) who borrow materials. | Easy catalog search, self-service holds/renewals, borrowing history tracking, fine notifications. |

---

## 4. High-Level Features

### 4.1 Authentication & Authorization
* **Role-Based Access Control (RBAC):** Distinct permission sets for Admin, Staff, and Member users.
* **User Profile Management:** Self-service profile updates, borrowing history view, and password resets.

### 4.2 Book & Catalog Management
* **Inventory Metadata:** Comprehensive book records including Title, Author, Publisher, Publication Year, ISBN, Genre, Copy Count, and Shelf Location.
* **Stock & Status Tracking:** Real-time status indicators (Available, Borrowed, Reserved, Maintenance/Lost).

### 4.3 Circulation & Desk Operations
* **Issue & Return Desk:** Quick process for librarians to issue or return books using Member ID and Book ID / ISBN.
* **Self-Service Renewals:** Members can request loan extensions if no active holds exist on the item.

### 4.4 Reservation & Queue System
* **Hold Queue:** Automated queuing system for requested books; automatically notifies the next user when the item is returned.
* **Hold Expiration:** Configurable hold pickup window before reservation advances to the next user in line.

### 4.5 Fines & Automated Notifications
* **Fine Calculator:** Automatic late fee computation based on overdue days and member type policies.
* **Notification System:** In-app and email notifications for issue confirmation, due date reminders (e.g., 2 days prior), overdue notices, and hold availability.

### 4.6 Search & Filter Engine
* **Advanced Search:** Multi-parameter search supporting keyword, title, author, genre, and publication year.
* **Availability Toggle:** Instant filtering for items currently available on shelves.

### 4.7 Dashboard & Reports
* **Administrative Analytics:** Graphical representation of circulation trends, active vs. dormant members, and monthly fine revenues.
* **Exportable Reports:** Export overdue lists, inventory audits, and transaction logs in CSV or PDF formats.