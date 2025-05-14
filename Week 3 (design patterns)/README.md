# Overview


A simple payment management system for user and transaction handling, enhanced with design patterns for improved structure and scalability.


# Important Features


`User Management:` Create Basic or Premium users with balance tracking and transaction limits (5/day for Basic, unlimited for Premium).


`Transaction Processing:` Supports Money Transfer, Bill Payment, and Mobile Recharge with PIN verification.


`Database Integration:` Stores user data, transactions, and PINs in an SQLite database (payment.db).


`Real-Time Notifications:` CLI displays transaction success/failure notifications via the Observer Pattern.


`Design Patterns:` Implements multiple patterns for better code organization and extensibility.


# Design Patterns Used


a. `Factory Method (transaction_controller.py):` Simplifies transaction creation (Money Transfer, Bill Payment, Mobile Recharge).


b. `Observer (payment.py, cli.py):` Notifies the CLI of transaction events (success/failure).


c. `Strategy (user.py):` Manages transaction policies for Basic and Premium users.


d. `Facade (main.py):` Provides a simplified interface for system operations.


e. `Singleton (connection.py, database.py):` Ensures single instances of database connections and operations.



# Notes


a. The database (payment.db) will be created automatically in the repository/ folder.

b. Ensure the repository/ directory is writable.
